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

def prompt():
	while True:
		x = input("Please enter goal pot value (between 0 and 1): ")
		if (x == "X" or x == "x"):
			return "quit"

		try:
			value = float(x)
			if (value < 0 or value > 1):
				print("Invalid input.")
			else:
				return value

		except ValueError:
			print("Invalid input.")

def inputPotGoal():
	# keeps track of where the x motor is in its stepper sequence
	seqStepX = 0
	seqStepY = 0

	while True:
		print("== X Motor Input ==")
		xPotGoal = prompt()
		if (xPotGoal == "quit"):
			return

		print("== Y Motor Input ==")
		yPotGoal = prompt()
		if (yPotGoal == "quit"):
			return

		print("\nMoving to pot value (", xPotGoal, ",", yPotGoal, ") ...")

		# Move until pot value is within tolerance of goal value
		xDiff = xPot.value - xPotGoal
		yDiff = yPot.value - yPotGoal


		while ((xDiff > tolerance or xDiff < -tolerance) or (yDiff > tolerance or yDiff < -tolerance)):
			#checks if x value is within bounds
			if (xDiff < tolerance or xDiff > -tolerance):
				seqStepX = takeStep(2, findDirection(xDiff), seqStepX)

			#checks if y value is within bounds
			if(yDiff < tolerance or yDiff > -tolerance):
				seqStepY = takeStep(1, findDirection(yDiff), seqStepY)

			#update the difference between where we are and where we want to go
			xDiff = xPot.value - xPotGoal
			yDiff = yPot.value - yPotGoal

		print("Arrived at pot value (", xPot.value, ",",  yPot.value, ")\n")

		# pause before allowing user input again
		t.sleep(2)

def main():
	inputPotGoal()

if __name__ == "__main__":
	main()
