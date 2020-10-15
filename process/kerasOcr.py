import os
import keras_ocr
from filterText import filterText

path = os.getcwd()
pipeline = keras_ocr.pipeline.Pipeline()

def kerasOcr():
    image = os.path.join(path, './image/ContainerNumber.jpg')
    images = keras_ocr.tools.read(image)
    predictions = pipeline.recognize([images])[0]
    text = [text.upper() for text, box in predictions]
    containerNumber = filterText(text)
    return containerNumber

text = kerasOcr()
print(text)