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

def moving():
    print("Thread 1 started.")
    time.sleep(5)  # Simulate a task that takes 5 seconds
    print("Thread 1 finished.")
    corners, ids, rejected = detector.detectMarkers(frame)
    if ids is not None:
        for i in range(len(ids)):
            tag_center_x = (corners[i][0][0][0] + corners[i][0][2][0]) / 2
            frame_center_x = frame.shape[1] / 2
            tolerance = 50
            if((tag_center_x - frame_center_x) < 50){
                distance = get_distance_tof() - 381
                
                #add in color to this dict later
                thisB = dict(id = ids[i], dist = distance)

                bList.append(thisB)
                m.rotate_clockwise(180)
            }
    

def scanning():
    print("Thread 2 started.")
    time.sleep(10)  # Simulate a task that takes 10 seconds
    print("Thread 2 finished.")

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
