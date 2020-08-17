import RPi.GPIO as GPIO

def run(action):
  GPIO.output(22, not action)
