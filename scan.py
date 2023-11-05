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

def scanning():
    time.sleep(5)  # Simulate a task that takes 5 seconds
    while True:
        m.send_keepalive()
        frame = m.get_frame_read().frame
        corners, ids, rejected = detector.detectMarkers(frame)

        if ids is not None:
            for i in range(len(ids)):
                tag_center_x = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
                frame_center_x = frame.shape[1] / 2
                tolerance = 50

                distance = m.get_distance_tof() - 381
                if (distance > 381):
                    break

                if((tag_center_x - frame_center_x) < 50):
                    
                    #add in color to this dict later
                    thisB = dict(id = ids[i], dist = distance)

                    bList.append(thisB)
    

def moving():
    m.move_left(381)

# Create two threads
move = threading.Thread(target=moving)
scan = threading.Thread(target=scanning)

# Start both threads at the same time
move.start()
scan.start()

# Wait for both threads to finish   
move.join()
scan.join()
     
print("Both threads have finished.")
print(bList)
