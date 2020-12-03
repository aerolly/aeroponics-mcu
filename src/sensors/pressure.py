import time
import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)

# port is in the form of p0 p1 p2 p3
def run(param=None):
    chan = AnalogIn(ads, ADS.P0)
    return chan.voltage * (150 / 5)
