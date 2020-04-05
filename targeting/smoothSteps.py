import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import math
import sys

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
	sleep(time)

	if(direction == 1):
		if (seqStep == 7):
			return 0
		else:
			return seqStep + 1
	else:
		if (seqStep == 0):
			return 7
		else:
			return seqStep - 1
def main():
	drawCircle = []
	angle = 0

	drawCircle.append([0,0,-1,1])
	for i in range(0,5):
		drawCircle.append([-1,1,1,1])
		drawCircle.append([1,1,1,-1])
		drawCircle.append([1,-1,-1,-1])
		drawCircle.append([-1,-1,-1,1])

	drawCircle.append([-1,1,0,0])

	while (angle > -360*5):
		x1 = math.cos(math.radians(angle))
		y1 = math.sin(math.radians(angle))
		angle = angle - 5
		x2 = math.cos(math.radians(angle))
		y2 = math.sin(math.radians(angle))
		drawCircle.append([x1, y1, x2, y2])

	drawCircle.append([x2,y2,0,0])

	seqStepX = 0
	seqStepY = 0
	radPerStep = (2.0 * math.pi) / 4076.0
	currentTheta = 0.0001
	currentPhi = 0.0001
	currentX = 0.0
	currentY = 0.0
	currentDX = math.sin(radPerStep) / math.cos(currentTheta)
	currentDY = math.sin(radPerStep) / math.cos(currentPhi)

	for lineDraw in drawCircle:
		for x in range(0, 2):
			nextX = float(lineDraw[x*2]) * scale
			nextY = float(lineDraw[x*2+1]) * scale
			
			dx = currentX - nextX
			dy = currentY - nextY
			stepsX = abs(dx / currentDX) * 2
			stepsY = abs(dy / currentDY) * 2

			if stepsX > stepsY:
				yStepArray = np.linspace(currentY, nextY, stepsX)
				xStepArray = np.linspace(currentX, nextX, stepsX)
			else:
				yStepArray = np.linspace(currentY, nextY, stepsY)
				xStepArray = np.linspace(currentX, nextX, stepsY)
			for i in range(0, len(xStepArray)):
				currentX = math.tan(currentTheta)
				currentY = math.tan(currentPhi)/math.cos(currentTheta)
				if abs(xStepArray[i] - currentX) > currentDX:
					if xStepArray[i] - currentX > 0:
						seqStepX = takeStep(2, 1, seqStepX)
						currentTheta = currentTheta + radPerStep
					else:
						seqStepX = takeStep(2, 2, seqStepX)
						currentTheta = currentTheta - radPerStep
				if abs(yStepArray[i] - currentY) > currentDY:
					if yStepArray[i] - currentY > 0:
						seqStepY = takeStep(1, 1, seqStepY)
						currentPhi = currentPhi + radPerStep
					else:
						seqStepY = takeStep(1, 2, seqStepY)
						currentPhi = currentPhi - radPerStep
	for pin in range(0,4):
		GPIO.output(x_pins[pin], False)
		GPIO.output(y_pins[pin], False)

if __name__ == "__main__":
	main()
