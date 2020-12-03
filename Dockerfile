FROM python:3.8-slim-buster

RUN apt-get update -y --no-install-recommends

# gcc compiler and opencv prerequisites
RUN apt-get -y --no-install-recommends install nano git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
	python3-opencv ca-certificates python3-dev git wget sudo  \
	cmake ninja-build && \
  rm -rf /var/lib/apt/lists/*

# Detectron2 prerequisites
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install cython
RUN pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

# Detectron2 - CPU copy
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/index.html

# EasyOCR
RUN python -m pip install git+git://github.com/jaidedai/easyocr.git

# Tesseract OCR
RUN apt-get update && apt-get -y --no-install-recommends install tesseract-ocr 
RUN python -m pip install pytesseract

RUN python -m pip install configparser numpy flask strsim python-stdnum pytz

COPY . /app
WORKDIR /app

RUN mkdir /images

EXPOSE 5003
ENTRYPOINT [ "python3" ] 
CMD [ "server.py"]
