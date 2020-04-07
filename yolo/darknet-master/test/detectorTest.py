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

    # cut to two decimal places
    return [dist, angle]

def doDetect():
    images = []
    with open('./data/test.txt', 'r') as imageList:
        images = imageList.readlines()

    count = 0
    totalTime = 0

    while True:
        startTime = time.time()
        if count is len(images):
            break

        curr = images[count].strip('\n')
        
        yolo_result = performDetect(curr, configPath = "./cfg/yolo-link.cfg",
                                        weightPath = "./weights/yolo-link_final.weights",
                                        metaPath = "./data/link.data",
                                        showImage = False,
                                        makeImageOnly = False, initOnly = False)
        
        coords = [-1, -1]
        real_location = [-1, -1]
        width = -1
        height = -1

        highestConfidence = 0.0

        for detected in yolo_result:
            if detected[0] == 'link' and detected[1] > highestConfidence:
                coords[0] = int(detected[2][0])
                coords[1] = int(detected[2][1])
                width = int(detected[2][2])
                height = int(detected[2][3])
                highestConfidence = detected[1]
        
        real_location = detectDistance(coords[0], coords[1], width, height)
        elapsed = time.time() - startTime

        print("File: {}, Coords: {}, Distance: {}, Angle: {}, Elapsed: {}".format(curr, coords, real_location[0], real_location[1], elapsed)) 
        count = count + 1
        totalTime = totalTime + elapsed

    print("Average time: {}".format(totalTime/count))

def main():
    doDetect()



if __name__ == '__main__':
    main()