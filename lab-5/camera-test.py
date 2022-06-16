#Description: Use OpenCV (cv2) and Video4Linux (V4L) to capture and store video frame 
#             as an jpg image
#Input :   USB based video class (UVC) device such as Logitech webcam C270
#Output :  Captured frame saved as file


import cv2

cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

ret, frame = cap.read()

cv2.imwrite('image.jpg', frame)

cap.release()
