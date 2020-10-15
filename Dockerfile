FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y

RUN apt-get install -y \
	python3 \
	python3-pip \
	cython \
	git \
	tesseract-ocr \
	libsm6 \
	python-tk

RUN echo "Installing Depedencies Detecton2"
RUN pip3 install -U torch==1.4+cu100 torchvision==0.5+cu100 -f https://download.pytorch.org/whl/torch_stable.html
# RUN pip3 install cython pyyaml==5.1
# RUN pip3 install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

# RUN echo "Installing Detectron 2 library"
# RUN pip3 install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu100/index.html

# RUN echo "Installing Tesseract ocr"
# RUN pip3 install pytesseract

# RUN echo "Installing EasyOcr"
# RUN pip3 install git+git://github.com/jaidedai/easyocr.git

# RUN pip3 install configparser numpy Opencv-python flask

# COPY . /app
# WORKDIR /app

# EXPOSE 5002
# ENTRYPOINT [ "python3" ] 
# CMD [ "app.py"]