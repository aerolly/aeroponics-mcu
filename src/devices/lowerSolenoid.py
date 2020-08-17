import RPi.GPIO as GPIO

def run(action):
  GPIO.output(27, not action)
