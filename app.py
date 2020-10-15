import cv2

# Function proces container number
import process.detectContainerNumber
from process.detectContainerNumber import predicContainerNumber
from process.cropImage import cropImage
from process.preProcessImage import processImage
from process.easyOcr import ocrEasyOcr
from process.tesseractOcr import tesseractOcr

def processing(image):
    resultContainerNumber = {}
    result = predicContainerNumber(image)
    if result != '':
        imageCropped = cropImage(result, image)
        preProcessedImage = processImage(imageCropped)
        image = preProcessedImage.copy()
        cv2.imwrite('preprocessing.jpg', preProcessedImage)
        cv2.imwrite('prediction.jpg', imageCropped)
        # Get Vertical or Horizontal image
        height = image.shape[0]
        width = image.shape[1]
        if height < width:
            # easyOcr
            resultEasyOcr, confidenceEasyOcr = ocrEasyOcr(image, rotate='horizontal')
            resultContainerNumber['easyOcr'] = [resultEasyOcr, confidenceEasyOcr]
            # tesseractOcr
            resultTesseract, cofidenceTesseract = tesseractOcr(image)
            resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]

        elif height > width:
            # easyOcr
            resultEasyOcr, confidenceEasyOcr = ocrEasyOcr(image, rotate='vertical')
            resultContainerNumber['easyOcr'] = [resultEasyOcr, confidenceEasyOcr]
            # tesseractOcr
            resultTesseract, cofidenceTesseract = tesseractOcr(image, psm=6)
            resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]
        
        return resultContainerNumber
    else:
        return 'No Container Number detected'
