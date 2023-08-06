from .strong_sort.utils.parser import get_config
from .strong_sort.strong_sort import StrongSORT
from .ocsort.ocsort import OCSort
from .bytetrack.byte_tracker import BYTETracker
import os
import sys

STONG_SORT_CONFIG = """
STRONGSORT:
  ECC: True              # activate camera motion compensation
  MC_LAMBDA: 0.995       # matching with both appearance (1 - MC_LAMBDA) and motion cost
  EMA_ALPHA: 0.9         # updates  appearance  state in  an exponential moving average manner
  MAX_DIST: 0.2          # The matching threshold. Samples with larger distance are considered an invalid match
  MAX_IOU_DISTANCE: 0.7  # Gating threshold. Associations with cost larger than this value are disregarded.
  MAX_AGE: 30            # Maximum number of missed misses before a track is deleted
  N_INIT: 3              # Number of frames that a track remains in initialization phase
  NN_BUDGET: 100         # Maximum size of the appearance descriptors gallery  
"""



def create_tracker(tracker_type, appearance_descriptor_weights, device, half):
    if tracker_type == 'strongsort':
        # initialize StrongSORT
        cfg = get_config()
        cfg.merge_from_str(STONG_SORT_CONFIG)

        strongsort = StrongSORT(
            appearance_descriptor_weights,
            device,
            half,
            max_dist=cfg.STRONGSORT.MAX_DIST,
            max_iou_distance=cfg.STRONGSORT.MAX_IOU_DISTANCE,
            max_age=cfg.STRONGSORT.MAX_AGE,
            n_init=cfg.STRONGSORT.N_INIT,
            nn_budget=cfg.STRONGSORT.NN_BUDGET,
            mc_lambda=cfg.STRONGSORT.MC_LAMBDA,
            ema_alpha=cfg.STRONGSORT.EMA_ALPHA,

        )
        return strongsort
    elif tracker_type == 'ocsort':
        ocsort = OCSort(
            det_thresh=0.45,
            iou_threshold=0.2,
            use_byte=False 
        )
        return ocsort
    elif tracker_type == 'bytetrack':
        bytetracker = BYTETracker(
            track_thresh=0.6,
            track_buffer=30,
            match_thresh=0.8,
            frame_rate=30
        )
        return bytetracker
    else:
        print('No such tracker')
        exit()