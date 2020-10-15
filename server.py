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