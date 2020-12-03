<<<<<<< HEAD
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
			if result.get('Container number') and len(result.get('Container number')) > 5:
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
=======
from flask import Flask, url_for, send_from_directory, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import logging, os
import cv2
import json
from app import processing

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.config['JSON_SORT_KEYS'] = False

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = '{}/images/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def createNewFolder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

def allowedFile(filename):
	namefile = filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	return namefile

def to_serializable(val):
	return str(val)

def getTimestamp():
	dateTime = datetime.now()
	timestamp = datetime.timestamp(dateTime)
	return timestamp

def processContainer(imgName):
	pathImage = os.path.join(app.config['UPLOAD_FOLDER'], imgName)
	image = cv2.imread(pathImage)
	res = processing(image)

	return res
	

@app.route('/api/v1/image-upload', methods = ['POST'])
def uploadImage():
	app.logger.info(PROJECT_HOME)
	if request.method == 'POST':
		try:
			request.files['image']
			app.logger.info(app.config['UPLOAD_FOLDER'])
			img = request.files['image']
			if allowedFile(img.filename):
				imgName = secure_filename(img.filename)
				createNewFolder(app.config['UPLOAD_FOLDER'])
				savedPath = os.path.join(app.config['UPLOAD_FOLDER'], imgName)
				app.logger.info("saving {}".format(savedPath))
				img.save(savedPath)
				# Process LPN
				result = processContainer(imgName)
				timestamp = getTimestamp()
				results = {	'message': 'success', 'image': imgName, 
							'timestamp': timestamp ,
							'containerNumber': result }
				return jsonify(results)
			else:
				return jsonify({'message': 'Please Uplod Image file only'})
		except KeyError:
			return jsonify({'message': 'Sample file Image missing in POST request'})
	else:
		return jsonify({'message': 'Sample file Image missing in POST request'})

if __name__ == '__main__':
	app.run(host ='0.0.0.0', port = 5005, debug = True)
>>>>>>> b75979ed493d7f8bfa25ba2180190d6f3a72020f
