import cv2
import numpy as np
from matplotlib import pyplot as plt

H = 'char/H.png'
S = 'char/S.png'

cap = cv2.VideoCapture(1) # 0 is the default camera of the laptop, 1 is the USB camera
template = cv2.imread(S, cv2.IMREAD_GRAYSCALE)

ret, binary = cv2.threshold(template, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('template', template)

while(True):
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	w, h = template.shape[::-1]
	res = cv2.matchTemplate(gray,template, 1)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

	top_left = min_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
	cv2.rectangle(frame,top_left, bottom_right, 255, 2)

	cv2.imshow('frame', frame)
	cv2.waitKey(25)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()