#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detecting lasers: Red circles with inner white fillings

@author: audi
"""
from PIL import Image as im
import numpy as np
import cv2
import sys
import time
#img = cv.imread('BLAH.png') #

'''
time per image
when it's not a circle
optimize the parameters to 

'''
'''
parameters for cv2.HoughCircles
input:
image	8-bit, single-channel, grayscale input image.
method	Detection method, see HoughModes. Currently, the only implemented method is HOUGH_GRADIENT
dp	Inverse ratio of the accumulator resolution to the image resolution. For example, if dp=1 , the accumulator has the same resolution as the input image. If dp=2 , the accumulator has half as big width and height.
minDist	Minimum distance between the centers of the detected circles. If the parameter is too small, multiple neighbor circles may be falsely detected in addition to a true one. If it is too large, some circles may be missed.
param1	First method-specific parameter. In case of HOUGH_GRADIENT , it is the higher threshold of the two passed to the Canny edge detector (the lower one is twice smaller).
param2	Second method-specific parameter. In case of HOUGH_GRADIENT , it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.
minRadius	Minimum circle radius.
maxRadius	Maximum circle radius. If <= 0, uses the maximum image dimension. If < 0, returns centers without finding the radius.

output:
circles	Output vector of found circles. Each vector is encoded as 3 or 4 element floating-point vector (x,y,radius) or (x,y,radius,votes) .

'''


'''
param1: 30 and 150 have similar results. hm
param2: higher, less circles:
'''
#    cv2.Smooth(gray, gray, cv2.CV_GAUSSIAN, 7, 7)


#draw the circles onto the frame
#circles is whether 1 by number of circles by 3 when num of circles >1 OR simply one d 3

def draw_circles(frame, circles):
    #print(circles.shape)
    print(circles)
    
    #shape = circles.shape
    #print(type(shape))
    #if len(circles == 0):
     #   print("Can't draw circles on frame because cirlces np array is empty")
    if circles.shape == (3,):  #one circle
        (x, y ,r) = circles
        cv2.circle(frame, (x, y), r, (255, 255, 255), 1)  #the circle
        cv2.circle(frame, (x, y), 2, (0, 0, 0), 3) #the nucleus
    elif circles.ndim == 3:#multiple circles"
        for (x, y ,r) in circles[0, :]:
            cv2.circle(frame, (x, y), r, (255, 255, 255), 1)  #the circle
            cv2.circle(frame, (x, y), 2, (0, 0, 0), 3) #the nucleus
    else:
        print("Can't draw circles on frame because cirlces np array is empty")

    
    cv2.imshow('frame',frame)


def filter_red(frame, circles): #1920*1080*3
    if circles.ndim == 1:#one circle
        return circles

    elif circles.ndim == 3:
        for circle in circles[0, :]: #cirlce = (x, y ,radius)
            x = int(circle[0])
            y = int(circle[1])
            r,g,b = frame[y,x] 
            white = (r > 220 and g > 220 and b > 220)
            red = (r > 120 and g > 40 and b > 60)
            if white or red:
                return circle
            
        print("failed to find white or red center")
        return np.asarray([])

        '''
        #for debugging only
        coord = (x,y)
        rgb = frame[y,x] 
        print("coord:" + str(coord) +  " rgb: " +  str(rgb) )
        '''
    else:
        print("Skipping filtering because function detect_cirlces detected no circles")
        #print(np.asarray([]))
        return np.asarray([])

        

def canny_edge(frame, val): #output a grayscale image of edges, easier for cv2.HoughCircles to detect circles
    ratio = 3
    kernel_size = 3
    low_threshold = val
    img_blur = cv2.blur(frame, (3,3))
    detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    dst = frame * (mask[:,:,None].astype(frame.dtype)) #numpy array 
    #cv2.imshow('edges', dst)
    return dst



def detect_circle(frame): # Display the resulting frame, WITH THE LASER CIRCLED
    edges = canny_edge(frame, 30) #if this num is too low, less circles detected and high chance of no circled deteced

    gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
    #gray = cv2.medianBlur(gray, 5)
    
    #print("detecting circles...")
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30,
    param1=30, param2=40, minRadius=0, maxRadius=50) #max 60 pixel circle #50 , param2 small = more false circles
    
    #print("cirlces:")
    #print(circles)
    
    #circles = np.uint16(np.around(circles))
    count = 0
    if circles is not None:
         ignore, count, ignore2 = circles.shape
         print("detected %s circle(s)" %count)
         
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




# Create a VideoCqapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('/Users/audi/Desktop/x1/Link_Laser_Samples/laser_sample_1/video.mp4')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
totoal_circles = 0
frames = 0
avg_circles_= 0

no_circle = 0


while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True: 
    #original_frame = np.copy(frame)
    detected_circles = detect_circle(frame)
    print(detected_circles)
    
    draw_circles(frame, detected_circles) #will modify frame to show the circles
    #time.sleep(2)
    #red_circle = filter_red(frame, detected_circles)
    #print(red_circle)
    #draw_circles(frame, red_circle) #will modify frame to show the circles
    #time.sleep(2)
    
    #DO SOME SUMMARY STATISTICS
    count = len(detected_circles)
    
    totoal_circles += count
    if count == 0:
        no_circle += 1
        
    frames += 1
    avg_circles = totoal_circles/frames
    no_circle_percent = no_circle/frames * 100
    
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("\nSUMMARY:")
        print("frames:", frames)
        print("%s average circles detected per frame" %round(avg_circles,2))
        print("%s percent of the time: Failed to identify any cirlce" %round(no_circle_percent,2) )
        break
  # Break the loop
  else:
    print("Failed to load frame:")
    break

 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()




'''

cap = cv2.VideoCapture("BLAH.mp4")
while(True):
    gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY),5)
    cirles=cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 10)# ret=[[Xpos,Ypos,Radius],...]
    if cirles!=None:print "Circle There !"
    cv2.imshow('video',gray)
    if cv2.waitKey(1)==27:# esc Key
        break
cap.release()
cv2.destroyAllWindows()

'''






'''
cap.read() returns a bool (True/False). If frame is read correctly, it will be True.
'''