import sys
import cv2
import pytz
import datetime
import os, os.path
import configparser
from glob import glob

try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

PATH  = config.get('Path Image', 'pathImage')

def getDatetime():
	IST = pytz.timezone('Asia/Jakarta')
	now = datetime.datetime.now(IST) 
	
	year    = str(now.year)[2:]
	month   = "0"+str(now.month) if len(str(now.month)) == 1 else str(now.month)
	day     = "0"+str(now.day) if len(str(now.day)) == 1 else str(now.day)
	hour    = "0"+str(now.hour) if len(str(now.hour)) == 1 else str(now.hour)
	minute  = "0"+str(now.minute) if len(str(now.minute)) == 1 else str(now.minute)
	
	datetimeDict = {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute}
	return datetimeDict

def pathImg(datetimeDict, truckId, gate, pos):
	gate = "0"+str(gate) if len(str(gate)) == 1 else str(gate)
	posCam = "0"+str(pos) if len(str(pos)) == 1 else str(pos)

	pathImage = ('{path}/images/Gate {gate}/{mm}/{dd}/{truckId}*{pos}.jpg'
				.format(path=PATH, gate=gate, mm=datetimeDict['month'], 
				dd=datetimeDict['day'], truckId=truckId, pos=posCam))

	return pathImage

def getImage(gate, posCam):
	dtDict = getDatetime()
	trukId = dtDict['year']+dtDict['month']+dtDict['day']+dtDict['hour']+dtDict['minute']
	PATH_IMG = pathImg(dtDict, trukId, gate, posCam)
	imgArr = []
	for img in glob(PATH_IMG):
		imgArr.append(img)
	return imgArr, trukId