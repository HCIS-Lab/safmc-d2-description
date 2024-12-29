import cv2 as cv
from cv2 import aruco

# dictionary to specify type of the marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

# MARKER_ID = 0
MARKER_SIZE = 400  # pixels

for id in range(40): 
    marker_image = aruco.generateImageMarker(marker_dict, id, MARKER_SIZE)
    cv.imwrite(f"markers/marker_{id}.png", marker_image)