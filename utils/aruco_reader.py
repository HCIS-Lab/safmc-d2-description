#####################################################################
### ArUco markers generated with generate-aruco-mark may not be   ###
### directly detected by this code due to the absence of padding. ###
### Adding a padding (like in aruco_0.png) to solve this problem. ###
#####################################################################
###            The ArUco here is using type DICT_5X5_50           ###
#####################################################################

import cv2

def main():
    frame = cv2.imread("aruco_0.png") # Replace this with the path to your target image file

    if frame is None:
        print("Unable to read the image file")
        return

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    show_image = False  # Whether to display the image

    # Detect ArUco markers
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

    # If markers are detected
    if markerIds is not None:
        for i, corner in enumerate(markerCorners):
            id = markerIds[i][0]
            print(f"Detected ArUco marker ID: {id}")

        if show_image:
            cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

    else:
        print("No ArUco markers detected")

    if show_image:
        cv2.imshow('ArUco Detection', frame)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
