from darknet import performDetect
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time

def getLinkCoords(img):
    yolo_result = performDetect(str(img), configPath = "./cfg/yolo-link.cfg",
                                    weightPath = "./weights/yolo-link_final.weights",
                                    metaPath = "./data/link.data",
                                    showImage = False,
                                    makeImageOnly = False, initOnly = False)
            
    coords = [-1, -1]

    highestConfidence = 0.0

    for detected in yolo_result:
        if detected[0] == 'link' and detected[1] > highestConfidence:
            coords[0] = int(detected[2][0])
            coords[1] = int(detected[2][1])
            highestConfidence = detected[1]

    return coords

def parseInput():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("--image", help = "Path to Image")
    args = arg_parse.parse_args()
    return args.image


def main():
    img = parseInput()
    link_coord = getLinkCoords(img)
    #laser_coord = getLaserCoords(img)
    print("Link Coordinates: ", link_coord)
    #print("Laser Coordinates", laser_coord)



if __name__ == '__main__':
    main()

