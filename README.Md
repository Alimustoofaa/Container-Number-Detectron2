# Install Detectron 2 Pytorch
## Dependencies
    $ pip install -U torch==1.4+cu100 torchvision==0.5+cu100 -f https://download.pytorch.org/whl/torch_stable.html
    $ pip install cython pyyaml==5.1
    $ pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
## Detectron 2 library
    $ pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu100/index.html


# Install Tesseract ocr
## Windows
    $ 
## Linux
    $ sudo apt install tesseract-ocr
## Pytesseract library
    $ pip install pytesseract


# Install EasyOcr
    $ pip install git+git://github.com/jaidedai/easyocr.git

# Run
    $ python server.py