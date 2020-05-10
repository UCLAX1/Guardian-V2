from yolo_mac.darknet import performDetect
#from yolo_pc.darknet import performDetect
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time



def detectDistance(x, y, w, h):

    imres = [960, 720]
    FOV = [62.2, 48.8]
    link = [5, 9]

    angular_width = (w / imres[0]) * FOV[0] * math.pi / 180
    dist = (link[0]/2) / math.tan(angular_width/2)
    angle = (x - (imres[0]/2)) * FOV[0] / imres[0]

    dist = float('%.2f'%(dist))
    angle = float('%.2f'%(angle))

    return (dist, angle)



def detect_link(frame):

    yolo_result = performDetect(frame, configPath = "./yolo_params/yolo-link.cfg",
        weightPath = "./yolo_params/yolo-link_final.weights",
        metaPath = "./yolo_params/link.data", showImage = False,
        makeImageOnly = False, initOnly = False)

    coords = (-1, -1)
    width = -1
    height = -1
    highestConfidence = 0.0

    for detected in yolo_result:
        if detected[0] == 'link' and detected[1] > highestConfidence:
            coords = (int(detected[2][0]), int(detected[2][1]))
            width = int(detected[2][2])
            height = int(detected[2][3])
            highestConfidence = detected[1]

    if coords == (-1, -1):
        coords = coords + (-1, -1)
    else:
        coords = coords + detectDistance(coords[0], coords[1], width, height)

    return coords
