import pytesseract
from pytesseract import Output
import configparser
import sys
from .filterText import filterText

try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

whiteList = config.get('Tesseract OCR', 'whitelist')

class TesseractOcr():
    def processOcr(image, psm):
        textConfArr = []
        custom_config = r'-c tessedit_char_whitelist={0} --psm {1}'.format(whiteList, psm)
        results = pytesseract.image_to_data(image,  lang='eng', config=custom_config, output_type=Output.DICT)
        for i in range(0, len(results["text"])):
            textConfArr.append([results["text"][i], float(int(results["conf"][i])/100)])
        
        return textConfArr

def tesseractOcr(image, psm=7):
    textConfArr = TesseractOcr.processOcr(image, psm)
    try:
        containerNumber, confidenceLevel = filterText(textConfArr)
    except ZeroDivisionError:
        containerNumber = ''.join([str(text) for text, conf in textConfArr])
        confidenceLevel = 0
    return containerNumber, confidenceLevel

# import cv2
# img = cv2.imread('process/container2.jpg')
# containerNumber, conf = tesseractOcr(img)
# print(' Container Number = {0} \n Confidende Level = {1}'.format(containerNumber, conf))
