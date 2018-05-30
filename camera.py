import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob

#empty lists to store template images
template_dataH=[]
template_dataS=[]
template_dataU=[]
temp_dirs=[]
letterFound=False

filesH = glob.glob('char/H/*.png')
filesS = glob.glob('char/S/*.png')
filesU = glob.glob('char/U/*.png')

temp_dirs.append(filesH)
temp_dirs.append(filesS)
temp_dirs.append(filesU)

#append the letters in each directory to it's list
for img in filesH:
    image = cv2.imread(img,0)
    template_dataH.append(image)
for img in filesS:
    image = cv2.imread(img,0)
    template_dataS.append(image)
for img in filesU:
    image = cv2.imread(img,0)
    template_dataU.append(image)


#printable data to debug
def print_template_data():    
	for dir in temp_dirs:
			for file in dir:
				print file



cap = cv2.VideoCapture(1) # 0 is the default camera of the laptop, 1 is the USB camera


while letterFound == False:

	for dir in temp_dirs:
		for temp in dir:

			letter = temp
			template = cv2.imread(temp, cv2.IMREAD_GRAYSCALE)
			template = cv2.blur(template, (10,10))

			ret, template = cv2.threshold(template, 160, 255, cv2.THRESH_BINARY)
			template = cv2.erode(template, None, iterations=2)
			template = cv2.dilate(template, None, iterations=2)

			ret, frame = cap.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			blur = cv2.blur(gray, (10,10))
			ret, binary = cv2.threshold(blur, 85, 255, cv2.THRESH_BINARY)
			binary = cv2.erode(binary, None, iterations=3)
			binary = cv2.dilate(binary, None, iterations=4)

			w, h = template.shape[::-1]
			res = cv2.matchTemplate(binary, template, cv2.TM_CCOEFF_NORMED)

			# Specify a threshold
			#0.7 was giving false readings on "U" while hunting for "H"
			#0.6 for non H
			#0.75 for H
			threshold = 0.75
			
			# Store the coordinates of matched area in a numpy array
			loc = np.where(res >= threshold) 

			#Checks if a letter was detected
			if np.amax(res) >= threshold:
				certainty = int(np.amax(res)*100)
				letterFound = True
				
			# Draw a rectangle around the matched region.
			for pt in zip(*loc[::-1]):
				cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)

			#Display frames
			cv2.imshow('template', template)
			cv2.imshow('binary', binary)
			cv2.imshow('frame', frame)
			cv2.waitKey(25)

		if letterFound:
			break
	#Quits if letter is found and prints what letter it detected
	if letterFound:
		print str(letter[5]) + " found with " + str(certainty) + "% certainty."
		break

	#Quits the program when "q" is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()