import RPi.GPIO as GPIO
import math as m

from RpiMotorLib import RpiMotorLib

GpioPins = [18, 23, 24, 25]
GpioPins2 = [17, 27, 22, 10]

mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
mymotortest2 = RpiMotorLib.BYJMotor("MyMotorTwo", "28BYJ")

delay = 0.001
r = 1
rad = 10;
x = [m.cos(i/m.pi) for i in range(20)]


#while True:
for i in range(dis):
	mymotortest.motor_run(GpioPins , delay, r, True, False, "half", 0.0)
	mymotortest2.motor_run(GpioPins2, delay, r, True, False, "half", 0.0) 
#	mymotortest.motor_run(GpioPins , delay, r, False, False, "half", 0.05)
#	mymotortest2.motor_run(GpioPins2 , delay, r, False, False, "half", 0.05)
for i in range(dis):
	mymotortest.motor_run(GpioPins , delay, r, True, False, "half", 0.0)
	mymotortest2.motor_run(GpioPins2, delay, r, False, False, "half", 0.0) 
for i in range(dis):
	mymotortest.motor_run(GpioPins , delay, r, False, False, "half", 0.0)
	mymotortest2.motor_run(GpioPins2, delay, r, False, False, "half", 0.0) 
for i in range(dis):
	mymotortest.motor_run(GpioPins , delay, r, False, False, "half", 0.0)
	mymotortest2.motor_run(GpioPins2, delay, r, True, False, "half", 0.0) 



GPIO.cleanup()
