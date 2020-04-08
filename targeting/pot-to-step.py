from gpiozero import MCP3008
import time as t
import RPi.GPIO as GPIO
import numpy as np
import math
import sys

xPot = MCP3008(channel=1)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

time = 0.00075
scale = 0.2

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
		return 2
    #negative difference means go positive direction
	elif (difference < 0):
		return 1
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
    xPotValue = xPot.value
    print("Current pot value for x motor: ", xPotValue, '\n')

    xSeqStep = 0
    for i in range(0,50):
        xSeqStep = takeStep(2, 1, xSeqStep)
        xPotValue = xPot.value
        print("Moved 1 step in positive direction, new x pot value: ",xPotValue, '\n')

    # moved back to original position
    for i in range(0,50):
        xSeqStep = takeStep(2,2,xSeqStep)
        xPotValue = xPot.value
        print("Moved x motor back to original position: ", xPotValue, '\n')

    n = input("Number of steps to take (pls put an int): ")
    n = int(n)

    oldX = xPot.value
    print("\nStarting pot value: ", oldX)

    # take n steps
    for i in range(n):
        xSeqStep = takeStep(2,1,xSeqStep)

    newX = xPot.value
    print("\nEnding pot value: ",newX)

    potDiff = newX - oldX
    potStep = potDiff/n
    print("\n",potDiff, " pot difference / ", n, " steps = ",potStep, " average pot values per step") 

if __name__ == "__main__":
	main()

    
