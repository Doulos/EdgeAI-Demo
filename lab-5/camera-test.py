#Description: Use OpenCV (cv2) and Video4Linux (V4L) to capture and store video frame 
#             as an jpg image
#Input :   USB based video class (UVC) device such as Logitech webcam C270
#Output :  Captured frame saved as file

import sys, time
import cv2

cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

i = 0

while cap.isOpened():
	success, frame = cap.read()
	if not success:
		sys.exit ('Error:Unable to read from webcam')
	image = (f'image{i}.jpg')
	cv2.imwrite(image, frame)
	i = i+1
	time.sleep(2)
cap.release()
