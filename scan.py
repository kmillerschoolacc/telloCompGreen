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

m.move_up(20)

m.move_back(381)
m.rotate_counter_clockwise(90)

while total_distance < 762:
    m.send_keepalive()
    frame = m.get_frame_read().frame
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
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        for i in range(len(ids)):
            tag_center_x = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
            frame_center_x = frame.shape[1] / 2
            if((abs(tag_center_x - frame_center_x)) < tolerance):
                if not any(d['id'] == thisB['id'] for d in bList):
                    bList.append(thisB)
                thisB = dict(id = ids[i], x = total_distance-762)
                print("tag centered")
                bList.append(thisB)
            if(abs((tag_center_x - frame_center_x)) > tolerance):
                print("tag not centered")
print(bList)
m.streamoff()
m.land()
