import argparse
from cv2 import aruco, imwrite


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate ArUco markers')
    parser.add_argument('-s', '--marker_size', type=int,
                        default=400, help='Size of the marker (in pixels)')
    parser.add_argument('-n', '--num_marker', type=int,
                        default=12, help='Number of markers to generate')
    parser.add_argument('-d', '--dict_type', type=str, default='DICT_5X5_50',
                        choices=['DICT_4X4_50', 'DICT_5X5_50', 'DICT_6X6_50', 'DICT_7X7_50',
                                 'DICT_5X5_100', 'DICT_5X5_250'],
                        help='The ArUco marker dictionary to use')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # dictionary to specify type of the marker
    dict_map = {
        'DICT_4X4_50': aruco.DICT_4X4_50,
        'DICT_5X5_50': aruco.DICT_5X5_50,
        'DICT_6X6_50': aruco.DICT_6X6_50,
        'DICT_7X7_50': aruco.DICT_7X7_50,
        'DICT_5X5_100': aruco.DICT_5X5_100,
        'DICT_5X5_250': aruco.DICT_5X5_250
    }
    marker_dict = aruco.getPredefinedDictionary(dict_map[args.dict_type])

    for id in range(args.num_marker):
        marker_image = aruco.generateImageMarker(
            marker_dict, id, args.marker_size)
        imwrite(f"markers/marker_{id}.png", marker_image)


if __name__ == "__main__":
    main()
