import threading
import time
import cv2
import numpy as np
from djitellopy import tello
import imutils
import random

idInp = int(input("id: "))
colorInp = str(input("color: "))

def getColor(raw_frame):
	rbgFrame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

	class color:
		def __init__(self, name, low, high):
			self.name = name
			self.low = low
			self.high = high

		def p(self):
			print(self.name, self.low, self.high)

	red = color("red", (50, 0, 0), (255, 20, 78))
	pink = color("pink", (182, 121, 157), (212, 173, 211))
	orange = color("orange", (182, 55, 0), (255, 147, 62))
	yellow = color("yellow", (169, 87, 0), (236, 255, 15))
	dark_green = color("dark_green", (0, 50, 0), (45, 176, 72))
	light_green = color("light_green", (88, 174, 74), (116, 255, 170))
	purple = color("purple", (102, 78, 150), (186, 122, 203))
	dark_blue =  color("dark_blue", (0, 11, 53), (23, 84, 255))
	light_blue = color("light_blue", (67, 132, 129), (99, 153, 175))

	colors = [red, pink, orange, yellow, dark_green, light_green, purple, dark_blue, light_blue]
	colorMasks = [0] * 9
	colorValues = [0] * 9

	raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)
	
	raw_frame = imutils.resize(raw_frame, width=960)
	rbgFrame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)
	cv2.imshow("frame", rbgFrame)
	for i in range(len(colors)):
		colorMasks[i] = cv2.inRange(raw_frame, colors[i].low, colors[i].high)
		colorMasks[i] = cv2.erode(colorMasks[i], None, iterations=5)
		colorMasks[i] = cv2.dilate(colorMasks[i], None, iterations=5)
		


	tolerance = 300 
	frame_center_x = rbgFrame.shape[1] / 2
	left = (int)(frame_center_x-tolerance)
	right = (int)(frame_center_x+tolerance)
	
	#frame = cv2.bitwise_and(raw_frame, raw_frame, mask=blueMask)
	for x in range(100):
		randomX = random.randint(left,right)
		randomY = random.randint(0,539)
		for i in range(len(colors)):
			colorValues[i] += colorMasks[i][randomY][randomX]/255
			
		colorFrame = colorMasks[colorValues.index(max(colorValues))]
		colorFrame = cv2.line(colorFrame, (left,539), (left,0), (255, 255, 255), 2)
		colorFrame = cv2.line(colorFrame, (right,539), (right,0), (255, 255, 255), 2)
		cv2.imshow("color", colorFrame)
    
	maxColor = colors[colorValues.index(max(colorValues))].name
	colorValues = [0] * 9
      
	return(maxColor)


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

m = tello.Tello()
m.connect()
m.streamon()
m.takeoff()

cameraMatrix = [
    (1.19047150e+03, 0.00000000e+00, 1.87149339e+02),
    (0.00000000e+00, 1.19046273e+03, 2.64741303e+02),
    (0.00000000e+00, 0.00000000e+00, 1.00000000e+00)
]
cameraMatrix = np.array(cameraMatrix)
dist = np.array([-0.03765726, 0.57115696, 0.01464739, -0.01555104, -2.51111791])

marker_length = 0.0762

bList = []
total_distance = 0

m.move_up(20)

m.move_back(381)
m.rotate_counter_clockwise(90)

while total_distance < 762:
    m.send_keepalive()
    frame = m.get_frame_read().frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame)

    tolerance = 300
    cv2.imshow("frame", frame)
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    frame_center_x = frame.shape[1] / 2
    lower_threshold = int(frame_center_x - tolerance)
    upper_threshold = int(frame_center_x + tolerance)
    cv2.line(frame, (lower_threshold, 0), (lower_threshold, frame.shape[0]), (0, 0, 255), 2)
    cv2.line(frame, (upper_threshold, 0), (upper_threshold, frame.shape[0]), (0, 0, 255), 2)
    
    m.move_right(31)
    total_distance += 30

    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, cameraMatrix, dist)
        camDistance = np.linalg.norm(tvecs[0])

        if len(ids) > 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, cameraMatrix, dist)
            camDistance = np.linalg.norm(tvecs[0])

        for i in range(len(ids)):
            tag_center_x = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
            frame_center_x = frame.shape[1] / 2
            if((abs(tag_center_x - frame_center_x)) < tolerance):
                thisB = dict(id = ids[i], x = camDistance/30.48, y = (total_distance-762)/30.48, color = getColor(frame))
                if not any(d['id'] == thisB['id'] for d in bList):
                    bList.append(thisB)
                    print(thisB)
                print("tag centered")
            if(abs((tag_center_x - frame_center_x)) > tolerance):
                print("tag not centered")

m.rotate_clockwise(180)
total_distance = 0

while total_distance < 762:
    m.send_keepalive()
    frame = m.get_frame_read().frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame)

    tolerance = 300
    cv2.imshow("frame", frame)
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    frame_center_x = frame.shape[1] / 2
    lower_threshold = int(frame_center_x - tolerance)
    upper_threshold = int(frame_center_x + tolerance)
    cv2.line(frame, (lower_threshold, 0), (lower_threshold, frame.shape[0]), (0, 0, 255), 2)
    cv2.line(frame, (upper_threshold, 0), (upper_threshold, frame.shape[0]), (0, 0, 255), 2)
    
    m.move_right(31)
    total_distance += 30

    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, cameraMatrix, dist)
        camDistance = np.linalg.norm(tvecs[0])

        if len(ids) > 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, cameraMatrix, dist)
            camDistance = -1 * np.linalg.norm(tvecs[0])

        for i in range(len(ids)):
            tag_center_x = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
            frame_center_x = frame.shape[1] / 2
            if((abs(tag_center_x - frame_center_x)) < tolerance):
                thisB = dict(id = ids[i], x = camDistance/30.48, y = (total_distance-762)/30.48, color = getColor(frame))
                if not any(d['id'] == thisB['id'] for d in bList):
                    bList.append(thisB)
                print("tag centered")
                bList.append(thisB)
            if(abs((tag_center_x - frame_center_x)) > tolerance):
                print("tag not centered")

for thisB in bList:
    if (thisB["id"] == idInp and thisB["color"] == colorInp):
        if (thisB["x"] < 0):
                m.rotate_clockwise(180)
                m.move_right(thisB["x"] * 30.48)
                m.move_forward(381)
        else:
                m.move_left(thisB["x"] * 30.48)
                m.move_forward(381)

print(bList)
m.streamoff()
m.land()
