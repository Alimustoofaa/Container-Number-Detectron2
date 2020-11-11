import os
import cv2
from glob import glob
from app import processing
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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
	result = processing(image, imageName, posCam)
	return result if type(result) == dict else {'error': result}

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
	for img in glob(imgPath):
		imgName = os.path.split(img)[-1]
		posCam = imgName[17:19]
		result = switchProcess(img, posCam)
		if result is not None:
			if result.get('Container number'):
				resultArr.append(result)
	if len(resultArr) != 0:
		confArr = [i['Confidence level'] for i in resultArr]
		keyMax = max(range(len(confArr)), key=confArr.__getitem__)
		return resultArr[keyMax]
	else:
		return None

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
			result = getImageForProcessing(truckId)
			if result is None:
				return jsonify({"error": "No container number"}), 400
			elif len(result) == 0:
				return jsonify({"error": "No image in path"}), 400
			return jsonify({"success":"", "time": datetime.now(), "results": result})
		except KeyError as e:
			return jsonify({"error": "Invalid mame"}), 400

if __name__=='__main__':
	app.run(host ='0.0.0.0', port = 5003, debug = True)
