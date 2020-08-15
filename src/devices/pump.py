import RPi.GPIO as GPIO

def run(control):
  GPIO.output(17, control)
