import os
import cv2
from app import processing
from werkzeug.exceptions import BadRequest
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowedFile(filename):
    try:
	    namefile = filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	    return namefile
    except IndexError as error:
        return None

def getPathImage(filename):
    path = '/home/prio/Downloads/HALOTEC'
    charName = os.path.splitext(filename)[0]
    month = charName[2:4]
    day = charName[4:6]
    pathImage = ('{path}/images/Gate 08/{mm}/{dd}/{trukId}'
                .format(path=path, mm=month, dd=day, trukId=filename))
    return pathImage

def process(filename):
    imgPath = getPathImage(filename)
    image = cv2.imread(imgPath)
    if image is not None:
        result = processing(image)
        return result
    else:
        return None

@app.route("/name", methods=["POST"])
def setName():
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
            return jsonify({"error": "Invalid email"}), 400

if __name__=='__main__':
    app.run(debug=True)