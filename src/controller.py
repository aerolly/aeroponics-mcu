import RPi.GPIO as GPIO
import time
import os
import controller as controller_methods
import requests
import simplejson as json

import settings

controllers = {}

try:
  response = requests.get(f'{os.getenv("API_IP")}/controller', timeout=2)

  for controller in json.loads(response.json()):
    controllers[f'{controller["NodeName"]}-{controller["ModuleName"]}-{controller["DeviceTypeName"]}'] = controller['CurrentDeviceGPIO']

  f = open('controllers.json', 'w')
  f.write(json.dumps(controllers))
  f.close()
except requests.exceptions.ConnectionError:
  print('Connection error.')
  f = open('controllers.json', 'r')
  controllers = json.loads(f.read())
  f.close()

def init(pin):
  GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

def run(pin, options):
  action = options['action']

  if action == 1:
    GPIO.output(pin, 0)
  elif action == 0:
    GPIO.output(pin, 1)

  # for automatic scheduling
  if 'waitTime' in options:
    time.sleep(options['waitTime'])
    # negative logic, so we reverse the passed in action
    GPIO.output(pin, action)
    action = not action

  return action

def deinit(pin):
  GPIO.cleanup(pin)
    