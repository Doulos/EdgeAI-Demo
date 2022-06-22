# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using PyCoral to detect objects in a given image.

To run this code, you must attach an Edge TPU attached to the host and
install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
device setup instructions, see coral.ai/docs/setup.

"""

#Reference code : https://github.com/google-coral/examples-camera/blob/master/opencv/detect.py

import argparse
import time
import cv2
import numpy as np

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


def draw_objects(draw, objs, labels):
	"""Draws the bounding box and label for each object."""
	for obj in objs:
		bbox = obj.bbox
		draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],outline='red')
		draw.text((bbox.xmin + 10, bbox.ymin + 10),'%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),fill='red')



def main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-m', '--model',
			help='File path of .tflite file',
					default='mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
	parser.add_argument('-i', '--input',
			help='File path of image to process')
	parser.add_argument('-l', '--labels', help='File path of labels file',
	default = 'coco_labels.txt')
	parser.add_argument('-t', '--threshold', type=float, default=0.1,
			help='Score threshold for detected objects')
	parser.add_argument('-o', '--output', 
			help='File path for the result image with annotations')
	parser.add_argument('-c', '--count', type=int, default=1,
			help='Number of times to run inference')
	args = parser.parse_args()
	print(f'Loading {args.model} with {args.labels} labels.')

	cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

  # Continuously capture images from the camera and run inference
	while cap.isOpened():
		success, image_cap = cap.read()
		if not success:
			sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')
		
    # Convert the image from BGR to RGB as required by the TFLite model.
		rgb_image = cv2.cvtColor(image_cap, cv2.COLOR_BGR2RGB)
		image =  cv2.resize(rgb_image, (300,300))

		labels = read_label_file(args.labels) if args.labels else {}
		interpreter = make_interpreter(args.model)
		interpreter.allocate_tensors()
		image = np.asarray(image)

		print('----INFERENCE TIME----')
		for _ in range(args.count):
			start = time.perf_counter()
			common.set_input(interpreter, image)
			interpreter.invoke()
			inference_time = time.perf_counter() - start
			objs = detect.get_objects(interpreter, args.threshold, (0.12,0.21))  # Resize to 300 pixels
			print(f'{(inference_time * 1000):0.3f} ms')

		print('-------RESULTS--------')
		if not objs:
			print('No objects detected')

		for obj in objs:
			print(labels.get(obj.id, obj.id))
			print('  id:    ', obj.id)
			print('  score: ', obj.score)
			print('  bbox:  ', obj.bbox)

		if args.output:
			image = image.convert('RGB')
			draw_objects(ImageDraw.Draw(image), objs, labels)
			image.save(args.output)
			image.show()

	cap.release()

if __name__ == '__main__':
	main()
