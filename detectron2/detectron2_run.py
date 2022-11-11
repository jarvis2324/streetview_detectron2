import sys, os, distutils.core
import torch, detectron2
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
import detectron2

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import pandas as pd

# cv2.imshow("fig",im) 
# cv2.waitKey(0)
def pred(im,lat,lon):
    df = pd.DataFrame(columns = ['Class', 'Lat', 'Long'])
    cfg = get_cfg()
    # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(im)
    # look at the outputs. See https://detectron2.readthedocs.io/tutorials/models.html#model-output-format for specification
    print(outputs["instances"].pred_classes)
    # print(outputs["instances"].pred_boxes) 

    for c in outputs["instances"].pred_classes:
        if c.cpu().numpy() == 0:
            df = df.append({'Class' : 'Person', 'Lat' : lat, 'Long' : lon}, ignore_index = True)
    return df
if __name__ == '__main__':    
    im = cv2.imread("./test.jpg")
    lat = 0
    lon = 0 
    pred(im,lat,lon)   