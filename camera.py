import cv2
import numpy as np
from matplotlib import pyplot as plt

H = 'char/H.png'
S = 'char/S.png'

cap = cv2.VideoCapture(1) # 0 is the default camera of the laptop, 1 is the USB camera
template = cv2.imread(S, cv2.IMREAD_GRAYSCALE)

ret, template = cv2.threshold(template, 160, 255, cv2.THRESH_BINARY)
template = cv2.erode(template, None, iterations=2)
template = cv2.dilate(template, None, iterations=2)

cv2.imshow('template', template)

while(True):
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, binary = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY)
	binary = cv2.erode(binary, None, iterations=3)
	binary = cv2.dilate(binary, None, iterations=4)

	w, h = template.shape[::-1]
	res = cv2.matchTemplate(binary, template, cv2.TM_SQDIFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

	top_left = min_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
	cv2.rectangle(frame,top_left, bottom_right, 255, 2)

	cv2.imshow('frame', frame)
	cv2.imshow('binary', binary)
	cv2.waitKey(25)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()