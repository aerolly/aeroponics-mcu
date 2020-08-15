import time
import board 
import busio
i2c = busio.I2C(board.SCL, board.SDA) 
import adafruit_ads1x15.ads1115 as ads 
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)
print(chan.value, chan.voltage)

def printval(port):
    chan = AnalogIn(ads, ADS.port)
    print(chan.value, chan.voltage)