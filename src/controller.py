import RPi.GPIO as GPIO
import time

def init(pin):
  GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def run(pin, action):
  GPIO.output(pin, action)
  return action

def deinit(pin):
  GPIO.cleanup(pin)
    