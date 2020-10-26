import os
import sys
from os import path
import configparser
from numpy import genfromtxt
from similarity.damerau import Damerau

try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

fileName = config.get('Data Container', 'nameFile')

# check file
file = path.exists(fileName)
if not file:
    print('Please add file', fileName)
    sys.exit()

def getStringDistance(containerNum):
    damerau = Damerau()
    valDist = []
    cnArr = genfromtxt(os.path.join(fileName), delimiter=',', names=True, dtype=None, encoding=None)
    
    for text in cnArr:
        res = damerau.distance(containerNum, text[0])
        valDist.append(res)
    
    # Get text
    scoreMin = min(range(len(valDist)), key=valDist.__getitem__)
    containerNumber = cnArr[scoreMin][0]
    return containerNumber