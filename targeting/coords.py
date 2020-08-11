from picamera.array import PiRGBArray
from picamera import PiCamera
import base64
import cv2
import io
import os
import numpy as np
import threading
import time as t
import zmq

#imports for the ADC and servos
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import sys
#import Adafruit_ADS1x15
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

######################## ADC set up #########################
#i2c = busio.I2C(board.SCL, board.SDA)
#ads = ADS.ADS1115(i2c, address=0x49)

#x_pot = AnalogIn(ads, ADS.P0)
#y_pot = AnalogIn(ads, ADS.P1)

#adc = Adafruit_ADS1x15.ADS1115()
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

time = 0.001 #75
scale = 0.2
tolerance = 15
sampleCount = 1
GAIN = 1
seqStepX = 0
seqStepY = 0

###################### Stepper set up ############################3
x_pins = [18, 23, 24, 25]
y_pins = [17, 27, 22, 4]

for pin in x_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, False)

for pin in y_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, False)

StepCount1 = 8

Seq = [[],[],[],[],[],[],[],[]]
#Seq = range(0, StepCount1)
Seq[0] = [1, 0, 0, 0]
Seq[1] = [1, 1, 0, 0]
Seq[2] = [0, 1, 0, 0]
Seq[3] = [0, 1, 1, 0]
Seq[4] = [0, 0, 1, 0]
Seq[5] = [0, 0, 1, 1]
Seq[6] = [0, 0, 0, 1]
Seq[7] = [1, 0, 0, 1]
nSteps = range(0, 2)

####################### Functions for laser pointer control #########################

# return the direction that the stepper should step in
def findDirection(difference):
    #positive difference means go negative direction
	if (difference > 0):
		return 2
    #negative difference means go positive direction
	elif (difference < 0):
		return 1
    #no difference means don't move
	else:
		return 0

#specialized step function
def takeStep(motor, direction, seqStep):
	if (motor == 1):
        # y motor
		#print(type(Seq))
		#print(type(Seq[seqStep]))
		for pin in range(0, 4):
			xpin = y_pins[pin]
			if Seq[seqStep][pin] != 0:
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
	elif (motor == 2):
        # x motor
		#print(type(seqStep))
		#print(type(Seq[seqStep]))
		for pin in range(0,4):
			xpin = x_pins[pin]
			if Seq[seqStep][pin] != 0:
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
	t.sleep(time)

    # move in the positive direction
	if(direction == 1):
		if (seqStep == 7):
			return 0
		else:
			return seqStep + 1

    # move in the negative direction
	elif(direction == 2):
		if (seqStep == 0):
			return 7
		else:
			return seqStep - 1

    # if direction = 0, then don't move that motor
	else:
		pass

# Globals 
laser_coords = (-1, -1)
link_coords = (-1, -1)
prev_laser = (-1, -1)
prev_link = (-1, -1)

# Moving the stepper
def moveToCoords():
    while (True):
        #global vars
        global prev_link
        global prev_laser
        global seqStepX
        global seqStepY

        if laser_coords == prev_laser:
            continue

        #FOR TESTING PURPOSES, FIXING LINK'S COORDS TO THE CENTER
        link_coords = (480, 360)

        #get the coords from the tuple values provided
        linkXC = link_coords[0]
        linkYC = link_coords[1]
        linkXP = prev_link[0]
        linkYP = prev_link[1]

        laserXC = laser_coords[0]
        laserYC = laser_coords[1]
        laserXP = prev_laser[0]
        laserYP = prev_laser[1]

        #stop moving if we don't know where the laser is
        if(sum(laser_coords) + sum(prev_laser) == -4):
            #will make it go to the center later on using pots
            continue

        #stop moving if we don't kno where link is
        elif(sum(link_coords) + sum(prev_link) == -4):
            continue

        ################# Only get here if we have enough info to move the laser ########################3

        #if the curr laser coords are 0, use the prev as the curr ones
        elif(laserXC == -1 and laserYC == -1):
            laserXC = laserXP
            laserYC = laserYP

        #if the current link coords are not known
        if(linkXC == -1 and linkYC == -1):
            #prev coords are known cause we checked earlier
            linkXC = linkXP
            linkYC = linkYP

        #if the prev link coords are not 0, use those as the current coords
        if(linkXP != -1 and linkYP != -1):
            linkXC = linkXP
            linkYC = linkYP

        xDiff = laserXC - linkXC
        yDiff = laserYC - linkYC

        #x stepper
        if(abs(xDiff) >= tolerance):
            seqStepX = takeStep(2, findDirection(-xDiff), seqStepX)

         #y stepper
        if(abs(yDiff) >= tolerance):
            seqStepY = takeStep(1, findDirection(yDiff), seqStepY)

        prev_link = link_coords
        prev_laser = laser_coords


        #if the curr link coords are -1, but prev coords aren't, move to prev coords
        #elif(linkXC == -1 and linkYC == -1 and linkXP != -1 and linkYP != -1):
            #difference is between old link coords and laser current coords
        #    xDiff = linkXP - laserXC
        #    yDiff = linkYP - laserYC

            #x stepper
        #    if(xDiff < tolerance or xDiff > -tolerance):
        #        seqStepX = takeStep(2,findDirection(xDiff), seqStepX)

            #y stepper
        #    if(yDiff < tolerance or yDiff > -tolerance):
        #        seqStepY = takeStep(1,findDirection(yDiff), seqStepY)

        #if the current links coords are valid, go to them
        #elif(linkXC != -1 and linkYC != -1):
        #    xDiff = linkXC - laserXC
        #    yDiff = linkYC - laserYC

            #x stepper
        #    if(xDiff < tolerance or xDiff > -tolerance):
        #        seqStepX = takeStep(2,findDirection(xDiff), seqStepX)

            #y stepper
        #    if(yDiff < tolerance or yDiff > -tolerance):
        #        seqStepY = takeStep(1,findDirection(yDiff), seqStepY)

            #update the previous coords
        #    prev_link = link_coords


########################### Akaash's stuff ########################
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.0.145:5555')

targeting_socket = context.socket(zmq.SUB)
targeting_socket.bind('tcp://*:6666')
targeting_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

camera = PiCamera()
camera.resolution = (960, 720)
camera.framerate = 60
camera.vflip = True
camera.hflip = True

rawCapture = PiRGBArray(camera, size = (960, 720))

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
            laser_coords = (int(coords[0]), int(coords[1]))
            link_coords = (int(coords[2]), int(coords[3]))
            print("Iteration " + str(i))
            print("Laser Coords: " + str(laser_coords))
            print("Link Coords: " + str(link_coords))
            print("-----")
            i += 1

        except KeyboardInterrupt:
            break



def main():

    x1 = threading.Thread(target = send_frames, daemon = False)
    x2 = threading.Thread(target = receive_data, daemon = True)
    x3 = threading.Thread(target = moveToCoords, daemon = True)

    x1.start()
    x2.start()
    x3.start()

if __name__ == "__main__":
    main()
