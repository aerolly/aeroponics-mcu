import RPi.GPIO as GPIO

def run(action):
  GPIO.output(17, action)
  return action