#Use Debian Bookworm as base
#FROM --platform=linux/aarch64 debian:bookworm-slim
FROM --platform=$BUILDPLATFORM debian:bookworm-slim


#Choose Python 3.10 
FROM python:3.10-slim

# Set our working directory
WORKDIR /usr/src/app

# Copy requirements.txt first f
COPY requirements.txt requirements.txt

# pip install python deps from requirements.txt
RUN pip3 install -r requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY . ./

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

# object-detection will run when container starts up on the UNO Q device
CMD ["python","-u","src/object-detection-yolov10.py"]
