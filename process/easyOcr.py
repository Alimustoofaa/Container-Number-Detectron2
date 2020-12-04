import easyocr
import numpy as np
import configparser
import sys
from .filterText import filterText


try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

######################  Horizontal Config ######################
allowListHor       = config.get('Easy OCR Horizontal', 'allowList')
detailHor          = int(config.get('Easy OCR Horizontal', 'detail'))
batchSizeHor       = int(config.get('Easy OCR Horizontal', 'batchSize'))
textThresholdHor   = float(config.get('Easy OCR Horizontal', 'textThreshold'))
lowTextHor         = float(config.get('Easy OCR Horizontal', 'lowText'))
linkThresholdHor   = float(config.get('Easy OCR Horizontal', 'linkThreshold'))

######################  Vertical Config ######################
allowListVer       = config.get('Easy OCR Vertical', 'allowList')
detailVer          = int(config.get('Easy OCR Vertical', 'detail'))
decoderVer         = config.get('Easy OCR Vertical', 'decoder')
beamWidthVer       = int(config.get('Easy OCR Vertical', 'beamWidth'))
batchSizeVer       = int(config.get('Easy OCR Vertical', 'batchSize'))
textThresholdVer   = float(config.get('Easy OCR Vertical', 'textThreshold'))
lowTextVer         = float(config.get('Easy OCR Vertical', 'lowText'))
linkThresholdVer   = float(config.get('Easy OCR Vertical', 'linkThreshold'))
slopeThsVer        = float(config.get('Easy OCR Vertical', 'slopeThs'))
minSizeVer         = int(config.get('Easy OCR Vertical', 'minSize'))

reader = easyocr.Reader(['en'], gpu=False)

class EasyOcr():
    def extractText(bounds):
        textConfArr = []
        for bound in bounds:
            textConfArr.append([bound[1], bound[2]])
        return textConfArr

    def processOcrHor(image):
        result = reader.readtext(
            image, 
            detail = detailHor,
            batch_size = batchSizeHor,
            allowlist = allowListHor,
            text_threshold = textThresholdHor,
            low_text = lowTextHor,
            link_threshold = linkThresholdHor
        )
        return result

    def processOcrVer(image):
        result = reader.readtext(
            image, 
            decoder = decoderVer,
            beamWidth = beamWidthVer,
            detail = detailVer,
            batch_size = batchSizeVer,
            allowlist = allowListVer,
            text_threshold = textThresholdVer,
            low_text = lowTextVer,
            link_threshold = linkThresholdVer,
            slope_ths = slopeThsVer,
            min_size = minSizeVer
        )
        return result

def ocrEasyOcr(image, rotate='horizontal'):
    if rotate == 'vertical':
        result = EasyOcr.processOcrVer(image)
    else:
        result = EasyOcr.processOcrHor(image)

    if len(result) != 0:
        textConfArr = EasyOcr.extractText(result)
        try:
            # if rotate == 'vertical':
            #     containerNumber = ''.join([e for e,_ in textConfArr])
            #     confidenceLevel = sum(i for _, i in textConfArr) / len(textConfArr)
            # else:
            containerNumber, confidenceLevel = filterText(textConfArr)
        except ZeroDivisionError:
            containerNumber = ''.join([str(text) for text, conf in textConfArr])
            confidenceLevel = 0
        return containerNumber, confidenceLevel
    else:
        return None, None

# import cv2
# img = cv2.imread('process/container2.jpg')
# containerNumber, conf = ocrEasyOcr(img, rotate='vertical')
# print(' Container Number = {0} \n Confidende Level = {1}'.format(containerNumber, conf))