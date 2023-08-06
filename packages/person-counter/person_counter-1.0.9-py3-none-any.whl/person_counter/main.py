
from opencv_stream import VideoStreamer, FpsDrawer
from model import PersonCounterModel, PersonCounterOutput
import numpy as np



stream = VideoStreamer.from_webcam()
fps = FpsDrawer()

model = PersonCounterModel()


@stream.on_next_frame()
def index(frame: np.ndarray):
   
   result = model.predict(frame) 

   if result.is_ok():
      output: PersonCounterOutput = result.unwrap()
      output.draw(frame)
   else:
    raise result.exception

   fps.draw(frame)


stream.start()
