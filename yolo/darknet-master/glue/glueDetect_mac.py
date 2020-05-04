from darknet_mac import detect
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time

def linkDetect(imagePath):
    image = cv2.imread(imagePath)
    '''
    yolo_result = performDetect(image, configPath = "./cfg/yolo-link.cfg",
                                    weightPath = "./weights/yolo-link_final.weights",
                                    metaPath = "./data/link.data",
                                    showImage = False,
                                    makeImageOnly = False, initOnly = False)
    '''

    yolo_result = detect(net = "./weights/yolo-link_final.weights",
                         meta = "./data/link.data",
                         image = image)

    coords = [-1, -1]

    highestConfidence = 0.0

    for detected in yolo_result:
        if detected[0] == 'link' and detected[1] > highestConfidence:
            coords[0] = int(detected[2][0])
            coords[1] = int(detected[2][1])
            highestConfidence = detected[1]
    
    return coords

if __name__ == "__main__":
    print("Coords: {}".format(linkDetect('./data/train/video_frame_10.jpg')))