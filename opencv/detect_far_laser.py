#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:17:27 2020

@author: audi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:38:59 2020

@author: audi
"""


#run detect_red_laser. It is the master function that takes a frame and returns a tuple of (x,y) coordinates. returns (-1,-1) if failed to 
#find a laser
import numpy as np
import cv2
import math


def most_red(frame, circles): #1920*1080*3
    
    if circles.ndim == 1:#one circle
        return circles

    elif circles.ndim == 3:
        #red_circles = []
        result = np.asarray([])
        min_dist = float("inf")
        
        for circle in circles[0, :]: #cirlce = (x, y ,radius)
            x = int(circle[0])
            y = int(circle[1])
            r,g,b = frame[y,x] 
            
    
        
            rgb = frame[y,x] 
            rgb_pixel = rgb.reshape((1,1,3))
            hsv = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2HSV)
            h = hsv[0,0,0]
            s = hsv[0,0,1]
            v = hsv[0,0,2]
            
            #red = (h < 200) and (s < 110) and (v>100) 
            #if red:
            #red_detected+=1
            squares = (h-168)**2 + (s-137)**2 + (v-204.5)**2
            dist = math.sqrt( squares )
            #red_circles.append(circle)
            
            if dist < min_dist:
                #print("Found a better one!")
                result = circle
                min_dist = dist
                #print(min_dist)
   
        if result.shape != (3,) :
            return (-1,-1)
       
        
        coord = result[0:2]
        coord = tuple(coord)
        print(coord)
        return coord
                    
        #n = len(red_circles)
        #red_circles = np.array(red_circles).reshape(1,n,3)       
        #return red_circles
          
            #hsv range:  vide 1 first 84 frames result
            #h: 0-200 (0-170) mean: 81, median 90
            #s: 0-110 (0-85) mean: 10 median: 5. 36?
            #v: 120-255 (129-255) mean: 250, median 255 
    else:
        print("Skipping filtering because function detect_cirlces detected no circles")
        #print(np.asarray([]))
        return np.asarray([])
    
#given an image in np array form, make all the non-red or non-white pixels black and return that red only image. 
def preserve_red(frame):
    if frame is None:
        return None
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([50,0,138]) #50,0,100
    upper_red = np.array([180,174,256])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)    #(h < 180) and (s < 174) and (v<256) and (v>138) \
    only_red = cv2.bitwise_and(frame,frame, mask=red_mask)
    #Image.fromarray(only_red).save("only_red.jpeg")
    return only_red

#given a gray scale image, detects the circles inside that image and return the found circles in a numpy array.
def detect_circle(gray): # Display the resulting frame, WITH THE LASER CIRCLED
    if gray is None:
        return None
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=1, param2=13, minRadius=0, maxRadius=20) #max 60 pixel circle #50 , param2 small = more false circles
    count = 0
    if circles is not None:
         ignore, count, ignore2 = circles.shape
         #if count > 10: if too many adjust param1 for cann_edge and param2 
                
         #print("detected %s circle(s)" %count)

         
          #save the detected circles iamges for anaylysis:
         #im.save("./laser_circles" + str())
         
    else:
        print("Failed to detect laser in this frame, skip and continue")
        return np.asarray([])
   
    #print(circles)
    #print(circles.shape) #1 by how many circles by 3 (x, y, and radius)
    
    return circles
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
 
    
def detect_red_laser(frame):
    if frame is None:
        return None
    only_red = preserve_red(frame)
    gray = cv2.cvtColor(only_red, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.erode(gray, None, iterations=1) #2
    gray = cv2.dilate(gray, None, iterations=2) #iterations = 4
    detected_circles = detect_circle(gray)
    red_circle = most_red(only_red, detected_circles)
    return red_circle


    

    
    
    
