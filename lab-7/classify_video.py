#Reference code: https://github.com/tensorflow/examples/blob/master/lite/examples/image_classification/raspberry_pi/classify.py

#Description :  Function main consists of the argument parser and calls function run. 
#               Function run starts capturing video in while cap.isOpened loop and performs inference on images frames. 
#               Inference compute time does not include image capture and preprocessing time. 

"""label_image for tflite."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import time
import sys

import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

import cv2



def run(model_file: str, num_threads:int, label_file: str, input_mean, input_std ) -> None:


	cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)


  # Continuously capture images from the camera and run inference
	while cap.isOpened():
		success, image = cap.read()
		if not success:
			sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

		image = cv2.flip(image, 1)


    # Convert the image from BGR to RGB as required by the TFLite model.
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create TensorImage from the RGB image
		interpreter = tflite.Interpreter(
		model_path=model_file, num_threads=num_threads)
		interpreter.allocate_tensors()

		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()

    # check the type of the input tensor
		floating_model = input_details[0]['dtype'] == np.float32

    # NxHxWxC, H:1, W:2
		height = input_details[0]['shape'][1]
		width = input_details[0]['shape'][2]
		dsize = (width,height)
		#print ('Width is', width, 'Height is', height)
		img1 = cv2.resize(rgb_image,dsize)
		img = np.asarray(img1)


    # add N dim
		input_data = np.expand_dims(img, axis=0)
  



		if floating_model:
			input_data = (np.float32(input_data) - input_mean) / input_std

		interpreter.set_tensor(input_details[0]['index'], input_data)

		start_time = time.time()
		interpreter.invoke()
		stop_time = time.time()

		output_data = interpreter.get_tensor(output_details[0]['index'])
		results = np.squeeze(output_data)


		top_k = results.argsort()[-5:][::-1]
		labels = load_labels(label_file)

		for i in top_k:
			if floating_model:
				print(f'{float(results[i])}: {labels[i]}')
			else:
				print(f'{float(results[i])}: {labels[i]}'.format(float(results[i] / 255.0), labels[i]))
				
		
		print(f'time: {(stop_time-start_time)*1000 }ms')

        # Stop the program if the ESC key is pressed.
		if cv2.waitKey(1) == 27:
			break

	cap.release()
	



def load_labels(filename):
	with open(filename, 'r') as f:
		return [line.strip() for line in f.readlines()]


def main():
	parser = argparse.ArgumentParser()
	
	
	parser.add_argument(
      '--model_file',
      default='mobilenet_v1_1.0_224.tflite',
      help='.tflite model to be executed')
	parser.add_argument(
      '--label_file',
      default='labels.txt',
      help='name of file containing labels')
	parser.add_argument(
      '--input_mean',
      default=127.5, type=float,
      help='input_mean')
	parser.add_argument(
      '--input_std',
      default=127.5, type=float,
      help='input standard deviation')
	parser.add_argument(
      '--num_threads', default=None, type=int, help='number of threads')
	args = parser.parse_args()
	
	
	run(args.model_file, args.num_threads, args.label_file, args.input_mean, args.input_std )
	


if __name__ == '__main__':
	main()