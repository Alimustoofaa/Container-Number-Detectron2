import sys
import cv2
import time
import threading
import configparser
from pathImage import getImage
from app import processing
from flask import Flask, render_template, jsonify

app = Flask(__name__)
appRun = False

try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

minConfidence  = float(config.get('Min Confidence', 'minConfidence'))

def processContainer(gate, posCam):
    img, truk = getImage(gate, posCam)
    if len(img) != 0:
        for image in img:
            imageCon = cv2.imread(image)
            result = processing(imageCon)
            result['pathImage'] = image
            return result
    else:
        return None

@app.before_first_request
def runProcess():
    def run():
        '''
        Position camera container(posCam):
        > Back container  = 10
        > Front container = 1
        '''
        global appRun
        while appRun:
            result = processContainer(gate=8, posCam=10)
            if result is not None:
                if result['Confidence level'] < minConfidence:
                    result = processContainer(gate=8, posCam=1)
                print(result)
            time.sleep(20)
    thread = threading.Thread(target=run)
    thread.start()      

@app.route('/start')
def start():
    global appRun
    appRun = True
    thread = threading.Thread(target=runProcess)
    thread.start()
    return "started"

@app.route('/stop')
def stop():
    global appRun
    appRun = False
    return 'stopped'

@app.route('/')
def status():
    status = 'start' if appRun else 'stop'
    message = ('Process OCR Container Number is '+status+
             '\nPlease go to http://0.0.0.0:5000/start to start and'+
             '\nPlease go to http://0.0.0.0:5000/stop to stop')
    return message

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)