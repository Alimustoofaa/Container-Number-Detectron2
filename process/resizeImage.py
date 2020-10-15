import cv2
import configparser
import sys

try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

scalePercent = int(config.get('Resize Image', 'scalePercent'))

def resizeImage(img, scale=scalePercent):
  width = int(img.shape[1] * scalePercent / 100)
  height = int(img.shape[0] * scalePercent / 100)
  dim = (width, height)

  resize = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

  return resize