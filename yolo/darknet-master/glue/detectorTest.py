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

def doDetect():
    images = []
    with open('./data/test.txt', 'r') as imageList:
        images = imageList.readlines()

    imlocs = [ [20, 0], [16, -25], [19, -15], [17, -5], [25, 0], [30, 0], [20, 15], [27, 25] ]

    count = 0
    totalTime = 0
    d_offset_avg = 0
    a_offset_avg = 0

    while True:
        startTime = time.time()
        if count is len(images):
            break

        curr = images[count].strip('\n')
        
        yolo_result = performDetect(curr, configPath = "./cfg/yolo-glue.cfg",
                                        weightPath = "./weights/yolo-glue_final.weights",
                                        metaPath = "./data/glue.data",
                                        showImage = False,
                                        makeImageOnly = False, initOnly = False)
        
        coords = [-1, -1]
        detect_loc = [-1, -1]
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
        
        detect_loc = detectDistance(coords[0], coords[1], width, height)
        elapsed = time.time() - startTime

        d_offset = abs(float(detect_loc[0]) - imlocs[count][0])
        a_offset = abs(float(detect_loc[1]) - imlocs[count][1])

        print("File: {}, Coords: {}, Distance offset: {}, Angle offset: {}, Elapsed: {}".format(curr, coords, d_offset, a_offset, elapsed)) 
        count = count + 1
        totalTime = totalTime + elapsed

        d_offset_avg = d_offset_avg + d_offset
        a_offset_avg = a_offset_avg + a_offset

    print("Average time: {}, Average Distance offset: {}, Average Angle offset: {}".format(totalTime/count, d_offset_avg/count, a_offset_avg/count))

def main():
    doDetect()



if __name__ == '__main__':
    main()