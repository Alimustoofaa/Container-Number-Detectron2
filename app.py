import cv2
import configparser
import sys
# Function proces container number
from process.easyOcr import ocrEasyOcr
from process.cropImage import cropImage
from process.resizeImage import resizeImage
from process.getContrast import getContrast
from process.tesseractOcr import tesseractOcr
from process.preProcessImage import processImage
from process.detectContainerNumber import predicContainerNumber
from process.checkDigit import checkDigitNum
from process.stringDistance import getStringDistance

try:
	config = configparser.ConfigParser()
	config.read_file(open(r'config.txt'))
except OSError as error:
	print(error.strerror)
	sys.exit()

scalePercent = int(config.get('Resize Image', 'scalePercent'))
minContrast  = int(config.get('Min Contrast', 'minContrast'))

def processing(image, imageName, posCam):
	resultContainerNumber = {}
	result = predicContainerNumber(image)
	if result != '':
		imageCropped = cropImage(result, image)
		if imageCropped.shape[1] < scalePercent:
			resizedImage = resizeImage(imageCropped)
		else:
			resizedImage = imageCropped.copy()
		contrast = getContrast(resizedImage)
		if contrast > minContrast:
			preProcessedImage = processImage(imageCropped)
			image = preProcessedImage.copy()
		else:
			image = resizedImage.copy()
		
		# Get Vertical or Horizontal image
		height = image.shape[0]
		width = image.shape[1]
		if height < width:
			resultEasyOcr, confidenceEasyOcr = ocrEasyOcr(image, rotate='horizontal')
			getStrDist = getStringDistance(resultEasyOcr) if resultEasyOcr is not None else None
			checked = checkDigitNum(getStrDist) if resultEasyOcr is not None else None
			resultContainerNumber = {
				'Position cam' : posCam,
				'Image name' : imageName,
				'Container number': resultEasyOcr,
				'String distance': getStrDist,
				'Confidence level': confidenceEasyOcr,
				'Check digit':checked
			}
			# tesseractOcr
			# resultTesseract, cofidenceTesseract = tesseractOcr(image)
			# resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]

		else:
			resultEasyOcr, confidenceEasyOcr = ocrEasyOcr(image, rotate='vertical')
			getStrDist = getStringDistance(resultEasyOcr) if resultEasyOcr is not None else None
			checked = checkDigitNum(resultEasyOcr) if resultEasyOcr is not None else None
			resultContainerNumber = {
				'Position cam' : posCam,
				'Image name' : imageName,
				'Container number': resultEasyOcr,
				'String distance': getStrDist,
				'Confidence level ': confidenceEasyOcr,
				'Check digit':checked
			}
			# tesseractOcr
			# resultTesseract, cofidenceTesseract = tesseractOcr(image, psm=6)
			# resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]a
		
		return resultContainerNumber
	else:
		return 'No Container Number detected'
