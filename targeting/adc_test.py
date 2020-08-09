'''
ADS1115 Analog to Digital Converter
Description: Testing basic use case for 16bit ADC
'''

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from  adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x49)

chan = AnalogIn(ads, ADS.P1)

print("{:>5}\t{:>5}".format('raw','v'))

while True:
	print("{:>5}\t{:>5}".format(chan.value, chan.voltage))
	time.sleep(0.05)
