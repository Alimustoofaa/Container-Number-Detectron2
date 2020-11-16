import os
import cv2
import pytz
import logging
from glob import glob
from app import processing
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

IST 	= pytz.timezone('Asia/Jakarta')
date 	= datetime.now(IST)
year 	= str(date.year)
month 	= "0"+str(date.month) if len(str(date.month)) == 1 else str(date.month)
day 	= "0"+str(date.day) if len(str(date.day)) == 1 else str(date.day)

PATH_LOG = os.path.join('images/{year}/{month}/{day}/loging_{day}-{month}-{year}.log'
						.format(year=year, month=month, day=day))
try:
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.ERROR)
	logging.basicConfig(filename=PATH_LOG, level=logging.ERROR,
						format=f'%(asctime)s %(levelname)s : %(message)s')
except FileNotFoundError as error:
	None

def getPathImage(truckId):
	'''
		pattren path image = C:\images\year\month\day\truckId+posCam.jpg
	'''
	year 		= truckId[0:2]
	month 		= truckId[2:4]
	day 		= truckId[4:6]

	pathImage = os.path.join(('images/20{year}/{mm}/{dd}/{truckId}*.jpg'
				.format(year=year, mm=month, dd=day, truckId=truckId)))
	return pathImage

def process(img, posCam):
	imageName = os.path.split(img)[-1]
	image = cv2.imread(img)
	app.logger.info('Processing image : {imgName} '
					'Possition Camera : {poscam}'
					.format(imgName=imageName, poscam=posCam))
	result = processing(image, imageName, posCam)
	return result if type(result) == dict else None

def switchProcess(pathImg, posCam):
	if posCam == '10':
		return process(pathImg, posCam)
	elif posCam == '01':
		return process(pathImg, posCam)
	elif posCam == '02':
		return process(pathImg, posCam)
	else:
		None

def getImageForProcessing(truckId):
	imgPath = getPathImage(truckId)
	resultArr = []
	resultArrNull = []
	for img in glob(imgPath):
		imgName = os.path.split(img)[-1]
		posCam = imgName[17:19]
		app.logger.info('Image found : '+imgName)
		result = switchProcess(img, posCam)
		if result is not None:
			if result.get('Container number'):
				resultArr.append(result)
			else:
				resultArrNull.append(result)
	if len(resultArr) != 0:
		confArr = [i['Confidence level'] for i in resultArr]
		keyMax = max(range(len(confArr)), key=confArr.__getitem__)
		return resultArr[keyMax]
	else:
		return resultArrNull[0]

@app.route("/truckid", methods=["POST"])
def postTruckId():
	if request.method=='POST':
		try:
			truckId = request.form['truck-id']
			if truckId.isnumeric() == False:
				return jsonify({"error": "String image name not numeric"}), 400
			elif len(truckId) != 17:
				return jsonify({"error": "String image name not valid"}), 400
				
			# Processing container 
			app.logger.info('Truck id : '+truckId)
			result = getImageForProcessing(truckId)
			if result is None:
				return jsonify({"messege":"Error no container number", "time": datetime.now(IST), "results": result}), 400
			elif len(result) == 0:
				return jsonify({"message": "Error no image in path", "time": datetime.now(IST), "results": result}), 400
			return jsonify({"message":"Success", "time": datetime.now(IST), "results": result})
		except KeyError as e:
			return jsonify({"message": "Error invalid keyName", "time": datetime.now(IST)}), 400

if __name__=='__main__':
	host = '0.0.0.0'
	port = 5003
	print("Server running in http://{host}:{port}".format(host=host, port=port))
	app.run(host=host, port=port, debug=True)
