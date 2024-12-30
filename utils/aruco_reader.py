#####################################################################
### ArUco markers generated with generate-aruco-mark may not be   ###
### directly detected by this code due to the absence of padding. ###
### Adding a padding (like in aruco_0.png) to solve this problem. ###
#####################################################################
###            The ArUco here is using type DICT_5X5_50           ###
#####################################################################

import cv2
import numpy as np
from typing import List

def identify_aruco(frame: np.ndarray)->List[int]:
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    show_image = False  # Whether to display the image, only use for debug, can be removed when changing to ROS node
    
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame) # Detect ArUco markers

    id = [] # if aruco aren't detected, returns will be []
    
    if markerIds is not None: # If markers are detected
        for i, corner in enumerate(markerCorners):
            id.append(int(markerIds[i][0]))

        if show_image:
            cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

    if show_image:
        cv2.imshow('ArUco Detection', frame)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    return id

if __name__ == "__main__":
    frame = cv2.imread("aruco_0.png") # Replace this with the path to your target image file

    if frame is None:
        print("Unable to read the image file")
    else:
        id = identify_aruco(frame)
        if id == []:
            print("No ArUco markers detected")
        else:
            print(f"Detected ArUco marker ID: {id}")
