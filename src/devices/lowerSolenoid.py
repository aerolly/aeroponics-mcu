import RPi.GPIO as GPIO

def run(control):
  GPIO.output(27, control)
