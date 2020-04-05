import RPi.GPIO as GPIO
import math
#from gpiozero import LED

from RpiMotorLib import RpiMotorLib

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

x_pins = [18, 23, 24, 25]
y_pins = [17, 27, 22, 4]

x_motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
y_motor = RpiMotorLib.BYJMotor("MyMotorTwo", "28BYJ")

delay = 0.001

#led = LED(14)
#led.on()

GPIO.setup(14,GPIO.OUT)
GPIO.output(14,True)

def drawline(x_final,y_final):
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

x = 5

for i in range(0,5):
	for a in range(0,360,20):
#		drawline(x*math.cos(math.radians(a)),x*math.sin(math.radians(a)))
		drawline(x*math.sin(math.radians(a)),0.5)

GPIO.cleanup()
