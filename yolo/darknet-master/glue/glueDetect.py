from darknet import performDetect
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time

imres = [ 960, 720 ]
FOV = [ 62.2, 48.8 ]
link = [ 5, 9 ]

def detectDistance(x, y, w, h):
    #Calculate angular width of link figurine in radians
    angular_width = (w / imres[0]) * FOV[0] * math.pi / 180

    #Calculate distance and angle to link figurine
    dist = (link[0]/2) / math.tan(angular_width/2)
    angle = (x - (imres[0]/2)) * FOV[0] / imres[0]

    dist = '%.2f'%(dist)
    angle = '%.2f'%(angle)
    return [dist, angle]

def linkDetect(imagePath):
    image = cv2.imread(imagePath)
    yolo_result = performDetect(image, configPath = "./cfg/yolo-glue.cfg",
                                    weightPath = "./weights/yolo-glue_final.weights",
                                    metaPath = "./data/glue.data",
                                    showImage = False,
                                    makeImageOnly = False, initOnly = False)
        
    coords = [-1, -1]
    width = -1
    height = -1
    highestConfidence = 0.0

    for detected in yolo_result:
        if detected[0] == 'glue' and detected[1] > highestConfidence:
            coords[0] = int(detected[2][0])
            coords[1] = int(detected[2][1])
            width = int(detected[2][2])
            height = int(detected[2][3])
            highestConfidence = detected[1]
    
    coords.extend(detectDistance(coords[0], coords[1], width, height))

    # Return x and y of link bounding box as well as distance and offset angle of figurine
    return coords

if __name__ == "__main__":
    print("Coords: {}".format(linkDetect('./data/train/video_frame_10.jpg')))