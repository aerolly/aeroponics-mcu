import time
from rpi_ws281x import *
import argparse

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255 #this is max for PWM
LED_INVERT = False
LED_CHANNEL = 0

def growlights(intensity):
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(intensity, 0, intensity))# only turn on red and blue 
        strip.show()
        
