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

#directories
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


#get image from cameras and set resolutions
cap1 = cv2.VideoCapture(2)
cap1.set(3,352)
cap1.set(4,240)
cap2 = cv2.VideoCapture(1)
cap2.set(3,352)
cap2.set(4,240)


while letterFound == False:
	for dir in temp_dirs:
		for temp in dir:
			letter = str(temp[5])
			template = cv2.imread(temp, cv2.IMREAD_GRAYSCALE)
			template = cv2.blur(template, (10,10))

			ret, template = cv2.threshold(template, 160, 255, cv2.THRESH_BINARY)
			template = cv2.erode(template, None, iterations=2)
			template = cv2.dilate(template, None, iterations=2)

			#frame 1 image treatment
			ret1, frame1 = cap1.read()
			gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
			blur1 = cv2.blur(gray1, (10,10))
			ret1, binary1 = cv2.threshold(blur1, 85, 255, cv2.THRESH_BINARY)
			binary1 = cv2.erode(binary1, None, iterations=3)
			binary1 = cv2.dilate(binary1, None, iterations=4)
			
			#frame 2 image treatment
			ret2, frame2 = cap2.read()
			gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
			blur2 = cv2.blur(gray2, (10,10))
			ret2, binary2 = cv2.threshold(blur2, 85, 255, cv2.THRESH_BINARY)
			binary2 = cv2.erode(binary2, None, iterations=3)
			binary2 = cv2.dilate(binary2, None, iterations=4)



			#checking for letters in binary
			w, h = template.shape[::-1]
			res1 = cv2.matchTemplate(binary1, template, cv2.TM_CCOEFF_NORMED)
			res2 = cv2.matchTemplate(binary2, template, cv2.TM_CCOEFF_NORMED)

			# Specify a threshold
			#0.7 was giving false readings on "U" while hunting for "H"
			#0.6 for non H
			#0.75 for H
			if letter == "H":
				threshold = 0.75
			else:
				threshold = 0.6
			
			# Store the coordinates of matched area in a numpy array
			loc1 = np.where(res1 >= threshold)
			loc2 = np.where(res2 >= threshold) 

			#Checks if a letter was detected
			if np.amax(res1) >= threshold:
				certainty = int(np.amax(res1)*100)
				letterFound = True
				for pt in zip(*loc1[::-1]):
					cv2.rectangle(frame1, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)

			if np.amax(res2) >= threshold:
				certainty = int(np.amax(res2)*100)
				letterFound = True
				for pt in zip(*loc2[::-1]):
					cv2.rectangle(frame2, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)


			#Display frames
			cv2.imshow('template', template)
			cv2.imshow('binary1', binary1)
			cv2.imshow('binary2', binary2)
			cv2.imshow('frame1', frame1)
			cv2.imshow('frame2', frame2)
			cv2.waitKey(25)

		if letterFound:
			break
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	#Quits if letter is found and prints what letter it detected
	if letterFound:
		print letter + " found with " + str(certainty) + "% certainty."
		break

	#Quits the program when "q" is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap1.release()
cap2.release()
cv2.destroyAllWindows()