import threading
import time
import cv2
from djitellopy import tello


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

m = tello.Tello()
m.connect()
m.streamon()


m.takeoff()

bList = []

total_distance = 0

m.move_back(381)
m.turn_left

while total_distance < 762:
    m.send_keepalive()
    frame = m.get_frame_read().frame
    corners, ids, rejected = detector.detectMarkers(frame)

    m.move_left(30.5)
    total_distance += 30.5

    if ids is not None:
        for i in range(len(ids)):
            tag_center_x = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
            frame_center_x = frame.shape[1] / 2
            tolerance = 50


            if((tag_center_x - frame_center_x) < tolerance):
                thisB = dict(id = ids[i], x = total_distance)
                bList.append(thisB)
print(thisB)
    

    
    
