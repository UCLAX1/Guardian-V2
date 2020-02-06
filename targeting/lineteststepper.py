import RPi.GPIO as GPIO

from RpiMotorLib import RpiMotorLib

x_pins = [18, 23, 24, 25]
y_pins = [17, 27, 22, 10]

x_motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
y_motor = RpiMotorLib.BYJMotor("MyMotorTwo", "28BYJ")

delay = 0.01

def myRound(x):
	diff = x - int(x)
	if (diff >= 0.5):
		return int(x) + 1
	else:
		return int(x)

def drawline(x_final,y_final):
	m = y_final / x_final
	y_prev = 0
	for x in range(0,x_final+1):
		y = math.myRound(m*x)
		print(x,y, m*x)
		if (y_prev != y):
			y_motor.motor_run(y_pins, delay, 1, True, False, "half", 0.0) 
		x_motor.motor_run(x_pins, delay, 1, False, False, "half", 0.0)
		y_prev = y

x = 10
y = 5
drawline(x,y)


GPIO.cleanup()
