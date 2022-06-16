# Know more about dockerfile templates here: #https://www.balena.io/docs/learn/develop/dockerfile/
FROM balenalib/raspberrypi3-64-debian

FROM python:3.7

# Set our working directory
WORKDIR /usr/src/app

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt requirements.txt

COPY onnxruntime-1.8.0-cp37-cp37m-manylinux_2_17_aarch64.manylinux2014_aarch64.whl onnxruntime-1.8.0-cp37-cp37m-manylinux_2_17_aarch64.manylinux2014_aarch64.whl

# pip install python deps from requirements.txt on the resin.io build server
RUN pip3 install -r requirements.txt

RUN pip3 install "onnxruntime-1.8.0-cp37-cp37m-manylinux_2_17_aarch64.manylinux2014_aarch64.whl"

# This will copy all files in our root to the working  directory in the container
COPY . ./

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

# main.py will run when container starts up on the device
CMD ["python","-u","src/main-onnx.py"]
