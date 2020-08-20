import RPi.GPIO as GPIO
import time

def initController(pin):
  GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def run(action, pin):
  GPIO.output(pin, action)
  return action

def deinitController(pin):
  GPIO.cleanup(pin)
    