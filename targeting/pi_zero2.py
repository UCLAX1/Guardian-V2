"""
ASME X1 Robotics 2019-2020 Project - The Guardian Hexapod: Collector's Edition
Description: Vishal's Updated version with bootup laser centering function (not finalized yet)
"""

# Import Libraries
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import MCP3008
from picamera.array import PiRGBArray
from picamera import PiCamera
import Adafruit_ADS1x15 as ADS
import base64
import board
import busio
import cv2
import io
import numpy as np
import os
import RPi.GPIO as GPIO
import sys
import threading
import time
import zmq

# Socket Initialization
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.0.148:5555')

targeting_socket = context.socket(zmq.SUB)
targeting_socket.bind('tcp://*:6666')
targeting_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

# Raspberry Pi Camera Setup
imageResolutionX = 960
imageResolutionY = 720
camera = PiCamera()
camera.resolution = (imageResolutionX, imageResolutionY)
camera.framerate = 60
camera.vflip = True
camera.hflip = True

rawCapture = PiRGBArray(camera, size = (imageResolutionX, imageResolutionY))

# GPIO Pin Initialization
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#ADC setup
adc = ADS.ADS1115()
GAIN = 1
xMid = 0.5
yMid = 0.5

# Stepper Motor GPIO Pin Definition
x_pins = [18, 23, 24, 25]
y_pins = [17, 27, 22, 4]
for pin in x_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, False)
for pin in y_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, False)

# Stepper Motor Step Sequence Pattern
Seq = [[1, 0, 0, 0],
       [1, 1, 0, 0],
       [0, 1, 0, 0],
       [0, 1, 1, 0],
       [0, 0, 1, 0],
       [0, 0, 1, 1],
       [0, 0, 0, 1],
       [1, 0, 0, 1]]
seqStepX = 0
seqStepY = 0

laser_coords = (-1, -1)
link_coords = (-1, -1)
prev_laser = (-1, -1)
prev_link = (-1, -1)

# Constant Variables
pixelsPerStep = 5.0 # Determines amount of correction made per camera feedback
                    # (larger value = less movement to correct an error)
tolerance = 15 # Determines minimum amount of error allowed in laser position
               # (in units of pixels)
stepWaitTime = 0.05 # Determines speed of the move_to_coords() function
                    # (larger value = slower stepper motor movement)



def send_frames():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        try:
            image = frame.array
            encoded, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)
            rawCapture.truncate(0)

        except KeyboardInterrupt:
            break



def receive_data():
    global laser_coords, link_coords

    i = 1
    while(1):
        try:
            coords = targeting_socket.recv_string()
            coords = coords.split(",")
            laser_coords = (int(float(coords[0])), int(float(coords[1])))
            link_coords = (int(coords[2]), int(coords[3]))
            print("Iteration " + str(i))
            print("Laser Coords: " + str(laser_coords))
            print("Link Coords: " + str(link_coords))
            print("-----")
            i += 1

        except KeyboardInterrupt:
            break



def findDirection(difference):
	if (difference > 0):
		return 2
	elif (difference < 0):
		return 1
	else:
		return 0



def takeStep(motor, direction, seqStep):
	if (motor == 1):
		for pin in range(0, 4):
			xpin = y_pins[pin]
			if Seq[seqStep][pin] != 0:
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
	elif (motor == 2):
		for pin in range(0,4):
			xpin = x_pins[pin]
			if Seq[seqStep][pin] != 0:
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
	time.sleep(0.001)

	if(direction == 1):
		if (seqStep == 7):
			return 0
		else:
			return seqStep + 1
	elif(direction == 2):
		if (seqStep == 0):
			return 7
		else:
			return seqStep - 1
	else:
		pass

def center_on_start():

    print("Entered center on start\n")
    global seqStepX, seqStepY
    print("Global Variables\n")
    #get the current locations of the potentiometers
    xPot = adc.read_adc(0, GAIN)
    yPot = adc.read_adc(1, GAIN)

    print("Calculating difference\n")

    #get the differences
    xDiff = xPot - xMid
    yDiff = yPot - yMid

    print("xDiff:" + str(xDiff) + "\n")

    while (abs(xDiff) > 0.002) or (abs(yDiff) > 0.002):
        if(abs(xDiff) > 0.002):
            seqStepX = takeStep(2, findDirection(xDiff), seqStepX)
            xPot = adc.read_adc(0, GAIN)
            xDiff = xPot - xMid

        if(abs(yDiff) > 0.002):
            seqStepY = takeStep(1, findDirection(yDiff), seqStepY)
            yPot = adc.read_adc(1, GAIN)
            yDiff = yPot - yMid

    print("Finished centering")


def move_to_coords():
    global prev_link, prev_laser, seqStepX, seqStepY

    #center the laser before moving it to link (or glue)

    print("Centering on start\n")

    center_on_start()

    print("Finished centering\n")

    while (1):
        if laser_coords == prev_laser:
            continue

        #FOR TESTING PURPOSES, FIXING LINK'S COORDS TO THE CENTER
        link_coords = (imageResolutionX/2, imageResolutionY/2)

        linkXC = link_coords[0]
        linkYC = link_coords[1]
        linkXP = prev_link[0]
        linkYP = prev_link[1]

        laserXC = laser_coords[0]
        laserYC = laser_coords[1]
        laserXP = prev_laser[0]
        laserYP = prev_laser[1]

        if(sum(laser_coords) + sum(prev_laser) == -4):
            continue
        elif(sum(link_coords) + sum(prev_link) == -4):
            continue
        elif(laserXC == -1 and laserYC == -1):
            laserXC = laserXP
            laserYC = laserYP

        if(linkXC == -1 and linkYC == -1):
            linkXC = linkXP
            linkYC = linkYP
        if(linkXP != -1 and linkYP != -1):
            linkXC = linkXP
            linkYC = linkYP

        xDiff = laserXC - linkXC
        yDiff = laserYC - linkYC

        xSteps = xDiff / pixelsPerStep
        ySteps = yDiff / pixelsPerStep
        stepTol = tolerance / pixelsPerStep

        maxSteps = max(abs(xDiff), abs(yDiff)) / pixelsPerStep

        laserX = laserXC / pixelsPerStep
        laserY = laserYC / pixelsPerStep
        linkX = linkXC / pixelsPerStep
        linkY = linkYC / pixelsPerStep

        prev_link = link_coords
        prev_laser = laser_coords

        for i in range(int(maxSteps)):
            if(link_coords[0] != linkXC and link_coords[1] != linkYC):
                break

            if(abs(xSteps) >= stepTol):
                seqStepX = takeStep(2, findDirection(-xDiff), seqStepX)
                if(xSteps > 0):
                    xSteps -= 1
                else:
                    xSteps += 1

            if(abs(ySteps) >= stepTol):
                seqStepY = takeStep(1, findDirection(yDiff), seqStepY)
                if(ySteps > 0):
                    ySteps -= 1
                else:
                    ySteps += 1

            time.sleep(stepWaitTime)



def main():

    print("Starting Program")

    center_on_start()

    #x1 = threading.Thread(target = send_frames, daemon = False)
    #x2 = threading.Thread(target = receive_data, daemon = True)
    #x3 = threading.Thread(target = move_to_coords, daemon = True)
    #x3 = threading.Thread(target = center_on_start, daemon = True)

    #x1.start()
    #x2.start()
    #x3.start()

    print("Finished Program")



if __name__ == "__main__":
    main()
