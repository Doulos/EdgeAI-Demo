#!/bin/bash

# Show your Raspberry Pi OS version.
cat /etc/os-release

# Add TPU Debian package repository to your system:
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update packages on your Raspberry Pi OS.
sudo apt-get update

#Install the Edge TPU runtime
sudo apt-get install libedgetpu1-std

#install PyCoral as follows
sudo apt-get install python3-pycoral


