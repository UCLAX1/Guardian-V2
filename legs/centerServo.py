kit1, kit2 = None, None
try:
    from adafruit_servokit import ServoKit
except:
    print("Library failed")
try:
    kit1 = ServoKit(channels=16, address=0x40)
    kit2 = ServoKit(channels=16, address=0x41)


    for i in range(16):
        kit1.servo[i].angle = 90
        kit2.servo[i].angle = 90
except:
    print("Servo Disabled")
