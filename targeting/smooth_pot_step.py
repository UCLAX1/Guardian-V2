from gpiozero import MCP3008
import time as t
import RPi.GPIO as GPIO
import numpy as np
import math
import sys

xPot = MCP3008(channel = 1)
yPot = MCP3008(channel = 2)

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

time = 0.00075
scale = 0.2
tolerance = 0.001

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

def findDirection(difference):
    #positive difference means go negative direction
	if (difference > 0):
		return 1
    #negative difference means go positive direction
	elif (difference < 0):
		return 2
    #no difference means don't move
	else:
		return 0

def takeStep(motor, direction, seqStep):
	if (motor == 1):
        # y motor
		for pin in range(0, 4):
			xpin = y_pins[pin]
			if Seq[seqStep][pin] != 0:
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
	elif (motor == 2):
        # x motor
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

def main():
    # step/pot
    ratio = 4076/1024

    print("Current xPot: ",xPot.value, "\nCurrent yPot: ", yPot.value)
    xGoal = input("What is your target xPot value? ")
    yGoal = input("What is your target yPot value? ")

    xDiff = xGoal - xPot.value
    yDiff = yGoal - yPot.value

    big = max(abs(xDiff), abs(yDiff))
    small = min(abs(xDiff), abs(yDiff))

    # pot/pot * step/pot * [pot] = steps
    m = big/small * ratio
    small_prev = 0

    #max num of steps
    steps = int(abs(big) * m) 

    for i in range(0,steps+1):
        j = int(m*i+0.5)

    index = 0
    prev = 0
    while (true):

        j = int(index*m + 0.5)

        if (xPot.value > xGoal-0.005 and xPot.value < xGoal+0.005):
            break
        else:
            if(prev != j):
                takeStep()



