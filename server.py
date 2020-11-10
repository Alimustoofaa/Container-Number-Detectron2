import os
import cv2
import sys
import configparser
from app import processing
from flask import Flask, jsonify, request

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

try:
	config = configparser.ConfigParser()
	config.read_file(open(r'config.txt'))
except OSError as error:
	print(error.strerror)
	sys.exit()

path  = config.get('Path Image', 'pathImage')
numGate = config.get('Number Gate', 'gate')

def allowedFile(filename):
	try:
		namefile = filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
		return namefile
	except IndexError as error:
		return None

def getPathImage(filename, pos=10):
	'''
		pattren path image = C:\images\year\month\day\trukid.jpg
	'''
	gate 		= "0"+numGate if len(numGate) == 1 else numGate
	posCam 		= "0"+str(pos) if len(str(pos)) == 1 else str(pos)
	charName 	= os.path.splitext(filename)[0]
	year 		= charName[0:2]
	month 		= charName[2:4]
	day 		= charName[4:6]

	if posCam == '10':
		pathImage = os.path.join(('images/20{year}/{mm}/{dd}/{trukId}'
					.format(year=year, mm=month, dd=day, trukId=filename)))
		return pathImage
	elif posCam == '01':
		filename = charName[:17]+str(posCam)
		pathImage = os.path.join(('images/20{year}/{mm}/{dd}/{trukId}.jpg'
					.format(year=year, mm=month, dd=day, trukId=filename)))
		return pathImage

def process(filename, pos=10):
	imgPath = getPathImage(filename, pos=pos)
	image = cv2.imread(imgPath)
	if image is not None:
		result = processing(image)
		return result
	else:
		return None

@app.route("/image", methods=["POST"])
def postImageName():
	if request.method=='POST':
		try:
			imageName = request.form['image-name']
			allowedCheck = allowedFile(imageName)
			if allowedCheck:
				charName = os.path.splitext(imageName)[0]
				if charName.isnumeric() == False:
					return jsonify({"error": "String image name not numeric"}), 400
				elif len(charName) != 19:
					return jsonify({"error": "String image name not valid"}), 400
				
				# Processing container 
				result = process(imageName)
				if result is None:
					return jsonify({"error": "No image in path"}), 400
				return jsonify(result)
			elif allowedCheck is None:
				return jsonify({"error": "String not fromat file"}), 400
			else:
				return jsonify({"error": "Invalid string filename"}), 400
		except KeyError as e:
			return jsonify({"error": "Invalid mame"}), 400

if __name__=='__main__':
	app.run(host ='0.0.0.0', port = 5003, debug = True)
