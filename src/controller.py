import RPi.GPIO as GPIO
import time
import os
import controller as controller_methods
import requests
import simplejson as json

import settings

response = requests.get(f'{os.getenv("API_IP")}/controller', timeout=2)

controllers = {}

for controller in json.loads(response.text):
  controllers[f'{controller["ModuleName"]}-{controller["DeviceTypeName"]}'] = controller['CurrentDeviceGPIO']

def init(pin):
  GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

def run(pin, action):
  if action == 1:
    GPIO.output(pin, 0)
  elif action == 0:
    GPIO.output(pin, 1)

  return action
def deinit(pin):
  GPIO.cleanup(pin)
    