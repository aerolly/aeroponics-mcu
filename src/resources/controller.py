import RPi.GPIO as GPIO
import time
import os
import controller as controller_methods
import requests
import simplejson as json

import settings

"""Retrieve all controller metadata from the database and save it to a file for later use.
Store controllers being used in the runtime in memory in the controllers dictionary.
Also contains methods to modify the controller state.
"""

controllers = {}

try:
  # Get current system controllers
  response = requests.get(f'{os.getenv("API_IP")}/controller', timeout=2)

  # Insert into controllers variable
  for controller in json.loads(response.json()):
    controllers[f'{controller["NodeName"]}-{controller["ModuleName"]}-{controller["DeviceTypeName"]}'] = controller['CurrentDeviceGPIO']

  # Save updated list to json file
  f = open('controllers.json', 'w')
  f.write(json.dumps(controllers))
  f.close()
except requests.exceptions.ConnectionError:
  print('Connection error.')
  f = open('controllers.json', 'r')
  controllers = json.loads(f.read())
  f.close()

def init(pin):
  """Initialize controllers to have high logic (off).
  """
  GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

def run(pin, options):
  """Modify the GPIO logic.

  Parameters:
  pin - GPIO pin to modify
  options - options for the modification, including the action and waitTime.

  Returns:
  The state that it was modified to be changed to.
  """
  action = options['action']

  # Negative logic, so reverse numbers.
  if action == 1:
    GPIO.output(pin, 0)
  elif action == 0:
    GPIO.output(pin, 1)

  # for automatic scheduling - turns off device after x seconds.
  if 'waitTime' in options:
    time.sleep(options['waitTime'])
    # negative logic, so we reverse the passed in action
    GPIO.output(pin, action)
    action = not action

  return action

def deinit(pin):
  GPIO.cleanup(pin)
    