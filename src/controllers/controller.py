import RPi.GPIO as GPIO

class Controller:
  def __init__(self, pin, negativeLogic):
    print('constructing')
    self.pin = pin
    self.negativeLogic = negativeLogic

    if negativeLogic:
      GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
    else:
      GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
  
  def run(self, action):
    if self.negativeLogic:
      GPIO.output(self.pin, not action)
      return not action
    else:
      GPIO.output(self.pin, action)
      return action
  
  def __del__(self):
    GPIO.cleanup(self.pin)
    