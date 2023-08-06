from typing import Optional
import opencv_stream
import numpy as np
import torch
from pathlib import Path
import sys
import os

#    ##########################################################

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 strongsort root directory
WEIGHTS = ROOT / 'weights'

from person_counter.yolov5.models.common import DetectMultiBackend

from person_counter.yolov5.utils.general import non_max_suppression, scale_boxes
from person_counter.yolov5.utils.torch_utils import select_device
from person_counter.yolov5.utils.dataloaders import letterbox
from person_counter.yolov5.utils.general import check_img_size
from person_counter.trackers.multi_tracker_zoo import create_tracker
import cv2

class PersonCounterModel(opencv_stream.Model):
   def __init__(self) -> None:
        yolo_weights=WEIGHTS / 'yolov5s.pt'
        dnn=False # use OpenCV DNN for ONNX inference
        # model = Model()
        device = ''
        self.device = select_device(device)
        self.half=False  # use FP16 half-precision inference
        self.model = DetectMultiBackend(yolo_weights, device=self.device, dnn=dnn, data=None, fp16=self.half)
        self.augment=False  # augmented inference
        self.conf_thres=0.25
        self.iou_thres=0.45
        self.classes = 0
        self.agnostic_nms=False  # class-agnostic NMS
        self.max_det=1000
        self.tracker_list = []
        tracking_method='strongsort'
        reid_weights=WEIGHTS / 'osnet_x0_25_msmt17.pt'
        nr_sources = 1
        for i in range(nr_sources):
            tracker = create_tracker(tracking_method, reid_weights, self.device, self.half)
            self.tracker_list.append(tracker, )
            if hasattr(self.tracker_list[i], 'model'):
                if hasattr(self.tracker_list[i].model, 'warmup'):
                    self.tracker_list[i].model.warmup()
        self.outputs = [None] * nr_sources

        self.prev_frames: Optional[np.ndarray] = None  
        self.stride = self.model.stride
        imgsz=(640, 640)
        self.img_size = check_img_size(imgsz, s=self.stride)
        self.auto = True

   def preprocess(self, image: np.ndarray)->torch.Tensor:
        image = np.stack([letterbox(x, self.img_size, stride=self.stride, auto=self.auto)[0] for x in [image]])  # resize
        image = image[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
        image = np.ascontiguousarray(image)  # contiguous

        image = torch.from_numpy(image).to(self.device)
        image = image.half() if self.half else image.float()  # uint8 to fp16/32
        image /= 255.0  # 0 - 255 to 0.0 - 1.0
        if len(image.shape) == 3:
            image = image[None]
        return image    

   @opencv_stream.Option.wrap
   @torch.no_grad()
   def predict(self, image: np.ndarray) -> opencv_stream.Option:
      
      preprocessed_image = self.preprocess(image)
      pred: torch.Tensor = self.model(preprocessed_image, augment=self.augment)
      pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)
      # list of detections, on (n,6) tensor per image [xyxy, conf, cls]
      #   outputs
      detections = []
      for i, det in enumerate(pred):
        if (det is None or not len(det)):
            continue
        # Rescale boxes from img_size to im0 size
        det[:, :4] = scale_boxes(preprocessed_image.shape[2:], det[:, :4], image.shape).round()  # xyxy
    
        if hasattr(self.tracker_list[i], 'tracker') and hasattr(self.tracker_list[i].tracker, 'camera_update'):
                # if prev_frames[i] is not None and curr_frames[i] is not None:  # camera motion compensation
                    self.tracker_list[i].tracker.camera_update(self.prev_frames, image)
        self.outputs[i] = self.tracker_list[i].update(det.cpu(), image)            
        self.prev_frames = image

        if len(self.outputs[i]) > 0:
          for j, (output, conf) in enumerate(zip(self.outputs[i], det[:, 4])):
            bboxes = output[0:4]
            id = output[4]
            cls = output[5]

            detections.append({"bboxes": [int(x) for x in bboxes], "id": int(id), "class": self.model.names[int(cls)], "confidence": float(conf) })

      return PersonCounterOutput(detections)

class PersonCounterOutput(opencv_stream.ModelOutput):

   def __init__(self, detections:list) -> None:
      self.detections = detections
     
 
   def to_dict(self) -> dict:
      return {k : v for k ,v in enumerate(self.detections)}

   def draw(self, image: np.ndarray) -> None:

        color = (0,0, 255)
        txt_color = (0,0,0)
        line_width = max(round(sum(image.shape) / 2 * 0.003), 2)
        for detection in self.detections:

            box = detection['bboxes']    
            p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))

            cv2.rectangle(image, p1, p2, color, thickness=line_width, lineType=cv2.LINE_AA)
            
            label = f"{detection['class']} {detection['confidence']:.2f} {detection['id']}"
            
            tf = max(line_width - 1, 1)  # font thickness
            w, h = cv2.getTextSize(label, 0, fontScale=line_width / 3, thickness=tf)[0]  # text width, height
            outside = p1[1] - h >= 3
            p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
            
            cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(image,
                        label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                        0,
                        line_width / 3,
                        txt_color,
                        thickness=tf,
                        lineType=cv2.LINE_AA)




