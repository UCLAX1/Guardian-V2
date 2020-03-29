from darknet import performDetect
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time

def doDetect():
    ''' This requires command line argument path, not what we want
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("--image", help = "Path to Image")
    args = arg_parse.parse_args()
    img = args.image
    '''

    images = []
    with open('./data/train.txt', 'r') as imageList:
        images = imageList.readlines()

    count = 0
    totalTime = 0

    while True:
        '''
        img_str = ""
        while True:
            data = camera_conn.recv(1024)
            img_str += data
            if "breakbreakbreak" in str(data):
                break
        print("Received Image")
        '''


        '''
        received_file = 'received_image.jpg'
        resized_file = 'resized_image.jpg'
    
        decoded_img = base64.b64decode(img_str.replace("breakbreakbreak", "")  + "===")
        
        with open(received_file, 'wb') as f:
            f.write(decoded_img)
        img = cv2.imread(received_file)

        resize_img = cv2.resize(img, (1280, 960))
        resize_img = cv2.resize(img, (960, 720))
        cv2.imwrite(resized_file, resize_img)

        b64_str = ""
        with open(resized_file, "rb") as imageFile:
            b64_str = base64.b64encode(imageFile.read())
        b64_str = b64_str + "breakbreakbreak"
        num_chunks = len(b64_str)/1024
        for i in range(0, num_chunks - 1):
            web_conn.send(b64_str[1024*i : 1024*(i + 1)])
        web_conn.send(b64_str[1024 * (num_chunks - 1) : ])
        print("Sent Image to Dashboard")

        location_data1, location_data2 = getLocations(img)
        controls_conn.send("clean" + location_data1)
        print(location_data1)
        camera_conn.send(location_data1)
        web_conn.send(location_data2)
        print("Sent Position Data to Pi 3 and Dashboard")
        print(" ")
        '''

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

        highestConfidence = 0.0

        for detected in yolo_result:
            if detected[0] == 'link' and detected[1] > highestConfidence:
                coords[0] = int(detected[2][0])
                coords[1] = int(detected[2][1])
                highestConfidence = detected[1]
        
        elapsed = time.time() - startTime

        print("File: {}, Coords: {}, Elapsed: {}".format(curr, coords, elapsed)) 
        count = count + 1
        totalTime = totalTime + elapsed

    print("Average time: {}".format(totalTime/count))

def main():
    doDetect()



if __name__ == '__main__':
    main()
