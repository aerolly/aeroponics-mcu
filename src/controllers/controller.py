import RPi.GPIO as GPIO
import time

class Controller:
  def __init__(self, pin, negativeLogic):
    print('constructing')
    self.pin = pin
    self.negativeLogic = negativeLogic

    if negativeLogic:
      GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
    else:
      GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
  
  def setOutput(self, action):
    if self.negativeLogic:
      GPIO.output(self.pin, not action)
      return not action
    else:
      GPIO.output(self.pin, action)
      return action

  def run(self, action):
    return self.setOutput(action)

  
  def __del__(self):
    GPIO.cleanup(self.pin)
    