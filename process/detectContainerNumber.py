import os
import sys
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo

path = os.getcwd()
try:
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file('COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml'))
    cfg.MODEL.DEVICE= 'cpu'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = os.path.join(path, 'models/model_final.pth')
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    predictor = DefaultPredictor(cfg)
except AssertionError as error:
    print(error)
    sys.exit()

def predicContainerNumber(image):
    outputs = predictor(image)
    if len(outputs["instances"].to("cpu").pred_boxes) != 0:
        return outputs
    else:
        return ''