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


# How to install with Docker?
## Download model and move to models/ repository
    $ https://drive.google.com/file/d/1-0IzZXcDo-3n7f01qw5g2YszSsWn7OE1/view?usp=sharing
## Build Dockefile
    $ docker build --tag named .
## Run
    $ docker run --name named -p 5002:5002 named

# How to start?
## Please edit Path Image in confix.text, change to your path