import cv2

# Function proces container number
from process.easyOcr import ocrEasyOcr
from process.cropImage import cropImage
from process.resizeImage import resizeImage
from process.getContrast import getContrast
from process.tesseractOcr import tesseractOcr
from process.preProcessImage import processImage
from process.detectContainerNumber import predicContainerNumber

def processing(image):
    resultContainerNumber = {}
    result = predicContainerNumber(image)
    if result != '':
        imageCropped = cropImage(result, image)
        resizedImage = resizeImage(imageCropped)
        contrast = getContrast(resizedImage)
        if contrast > 13:
            preProcessedImage = processImage(imageCropped)
            image = preProcessedImage.copy()
        else:
            image = resizedImage.copy()
        
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

        else:
            # easyOcr
            resultEasyOcr, confidenceEasyOcr = ocrEasyOcr(image, rotate='vertical')
            resultContainerNumber['easyOcr'] = [resultEasyOcr, confidenceEasyOcr]
            # tesseractOcr
            resultTesseract, cofidenceTesseract = tesseractOcr(image, psm=6)
            resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]
        
        return resultContainerNumber
    else:
        return 'No Container Number detected'
