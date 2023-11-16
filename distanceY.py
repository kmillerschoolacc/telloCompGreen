import numpy as np
import cv2 
from djitellopy import tello
import time

m = tello.Tello()
m.connect()
m.streamon()
m.takeoff()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

cameraMatrix = [
    (1.19047150e+03, 0.00000000e+00, 1.87149339e+02),
    (0.00000000e+00, 1.19046273e+03, 2.64741303e+02),
    (0.00000000e+00, 0.00000000e+00, 1.00000000e+00)
]
cameraMatrix = np.array(cameraMatrix)

#cameraMatrix = convert_to_matrix(tempCamMatrix)

dist = np.array([-0.03765726, 0.57115696, 0.01464739, -0.01555104, -2.51111791])

marker_length = 0.0762

while True:
    m.send_keepalive()
    frame = m.get_frame_read().frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame)

    if ids is not None and len(ids) > 0:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, cameraMatrix, dist)
        distance = np.linalg.norm(tvecs[0])

        print(f"Distance to ArUco marker with ID {ids[0]}: {distance} units")
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Display the frame
        cv2.imshow('Frame with ArUco', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
m.streamoff()
cv2.destroyAllWindows()
