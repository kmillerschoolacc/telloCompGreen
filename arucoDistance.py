import numpy as np
import cv2 


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

marker_length = 76.2  
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(frame)

    if ids is not None and len(ids) > 0:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, cameraMatrix=None, dist=None)
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
cap.release()
cv2.destroyAllWindows()
