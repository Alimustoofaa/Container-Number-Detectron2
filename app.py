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

def getDictResult(posCam, imageName, conNum=None, strDist=None, conLevel=None, checkDig=None):
	dictResult = {
			'Position cam' : posCam,
			'Image name' : imageName,
			'Container number': conNum,
			'String distance': strDist,
			'Confidence level': conLevel,
			'Check digit': checkDig
		}
	return dictResult

def processing(image, imageName, posCam):
	resultContainerNumber = {}
	result = predicContainerNumber(image)
	imageCropped = cropImage(result, image) if result != '' else image.copy()
	resizedImage = resizeImage(imageCropped) if imageCropped.shape[1] < scalePercent else imageCropped.copy()
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
		# log
		from server import app
		app.logger.info('OCR : '+resultEasyOcr if resultEasyOcr is not None else '-')
		try:
			getStrDist = getStringDistance(resultEasyOcr) if resultEasyOcr is not None or len(resultEasyOcr) == 0 else None
		except TypeError:
			getStrDist = None
		checked = checkDigitNum(getStrDist) if resultEasyOcr is not None else None
		resultContainerNumber = getDictResult(posCam, imageName, conNum=resultEasyOcr, strDist=getStrDist, conLevel=confidenceEasyOcr, checkDig=checked)
		# tesseractOcr
		# resultTesseract, cofidenceTesseract = tesseractOcr(image)
		# resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]
	else:
		resultEasyOcr, confidenceEasyOcr = ocrEasyOcr(image, rotate='vertical')
		try:
			getStrDist = getStringDistance(resultEasyOcr) if resultEasyOcr is not None or len(resultEasyOcr) == 0 else None
		except TypeError:
			getStrDist = None
		checked = checkDigitNum(getStrDist) if getStrDist is not None else None
		resultContainerNumber = getDictResult(posCam, imageName, conNum=resultEasyOcr, strDist=getStrDist, conLevel=confidenceEasyOcr, checkDig=checked)
		# tesseractOcr
		# resultTesseract, cofidenceTesseract = tesseractOcr(image, psm=6)
		# resultContainerNumber['tesseract'] = [resultTesseract, cofidenceTesseract]a
	return resultContainerNumber