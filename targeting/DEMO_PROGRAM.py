import RPi.GPIO as GPIO
import math
import random as rdm
#from gpiozero import LED

from RpiMotorLib import RpiMotorLib

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

x_pins = [18, 23, 24, 25]
y_pins = [17, 27, 22, 10]

x_motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
y_motor = RpiMotorLib.BYJMotor("MyMotorTwo", "28BYJ")

delay = 0.001

#led = LED(14)
#led.on()

GPIO.setup(14,GPIO.OUT)
GPIO.output(14,True)

def drawline(x_final,y_final):
	#x_final = int(x_final+0.5)
	#y_final = int(y_final+0.5)
	x_final = round(x_final)
	y_final = round(y_final)

	big =  max(abs(x_final),abs(y_final))
	small = min(abs(x_final), abs(y_final))
	x_big = abs(x_final) > abs(y_final)

	x_dir = x_final > 0
	y_dir = y_final > 0

	m = small / big
	small_prev = 0
	for i in range(0, abs(big+1)):
		j = int(m*i+0.5)
		if (small_prev != j):
			if (x_big):
				y_motor.motor_run(y_pins, delay, 1, y_dir, False, "half", 0.0)

			else:
				x_motor.motor_run(x_pins, delay, 1, not(x_dir), False, "half", 0.0)

		if (x_big): 
			x_motor.motor_run(x_pins, delay, 1, not(x_dir), False, "half", 0.0)

		else:
			y_motor.motor_run(y_pins, delay, 1, y_dir, False, "half", 0.0)
		small_prev = j

def drawCircle():
	drawline(0,-15)
	x = 5;
	for i in range(0,3):
		for a in range(0,360,20):
			drawline(x*math.cos(math.radians(a)),x*math.sin(math.radians(a)))
	drawline(0,15)

def drawNegCircle():
	drawline(0,-15)
	x = 5
	for i in range(0,3):
		for a in range(0,360,20):
			drawline(-x*math.cos(math.radians(a)),x*math.sin(math.radians(a)))
	drawline(0,15)

def drawEight():
	x = 4
	for i in range(0,2):
		for a in range(0,360,20):
			drawline(x*math.cos(math.radians(a)),x*math.sin(math.radians(a)))
		for a in range(0,360,20):
			drawline(x*math.cos(math.radians(-a)),x*math.sin(math.radians(-a)))

def drawStar():
	x = 30
	for i in range(30,70,30):
		for a in range(0,360,i):
			drawline(x*math.cos(math.radians(a)),x*math.sin(math.radians(a)))
			drawline(-x*math.cos(math.radians(a)),-x*math.sin(math.radians(a)))
	drawline(30,0)
	drawline(-30,0)

def drawSquare():
	drawline(0,-15)
	drawline(15,0)
	for i in range(0,4):
		drawline(0,30)
		drawline(-30,0)
		drawline(0,-30)
		drawline(30,0)
	drawline(0,15)
	drawline(-15,0)

#drawCircle()
#drawEight()
#drawStar()
#drawSquare()

p_choice = 0
while(True):
	random_choice = rdm.choice([1,2,3,4,5])
	while(random_choice == p_choice):
		random_choice = rdm.choice([1,2,3,4,5])
	p_choice = random_choice
	if random_choice == 1:
		drawCircle()
	elif random_choice == 2:
		drawEight()
	elif random_choice == 3:
		drawStar()
	elif random_choice == 4:
		drawSquare()
	elif random_choice == 5:
		drawNegCircle()
GPIO.cleanup()
