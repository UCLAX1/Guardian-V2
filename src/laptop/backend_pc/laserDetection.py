import cv2
import math
import numpy as np
import signal
import statistics as stat
import sys
import time



def canny_edge(frame, val):

    if frame is None:
        return None

    ratio = 13
    kernel_size = 3
    low_threshold = val
    img_blur = cv2.blur(frame, (3,3))

    detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    edges = frame * (mask[:,:,None].astype(frame.dtype))

    return edges



def detect_circle(frame):

    if frame is None:
        return None

    edges = canny_edge(frame, 30)
    gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=1, param2=13, minRadius=0, maxRadius=30)

    return circles



def filter_red(frame, circles):

    if circles is None:
        return (-1, -1)

    if circles.ndim == 1:
        return (int(circle[0]), int(circle[1]))

    elif circles.ndim == 3:
        result = np.asarray([])
        min_dist = float("inf")

        for circle in circles[0, :]:
            x = int(circle[0])
            y = int(circle[1])
            r,g,b = frame[y,x]

            rgb = frame[y,x]
            rgb_pixel = rgb.reshape((1,1,3))
            hsv = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2HSV)
            h = hsv[0,0,0]
            s = hsv[0,0,1]
            v = hsv[0,0,2]

            red = (h < 200) and (s < 110) and (v > 100)

            if red:
                squares = ((h - 81) ** 2) + ((s - 30) ** 2) + ((v - 250) ** 2)
                dist = math.sqrt(squares)

                if dist < min_dist:
                    result = circle
                    min_dist = dist

        if result.shape != (3,):
            return (-1, -1)

        return (int(result[0]), int(result[1]))

    else:
        return (-1, -1)



def detect_laser(frame):

	detected_circles = detect_circle(frame)
	red_circle = filter_red(frame, detected_circles)

	return red_circle
