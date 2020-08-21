import RPi.GPIO as GPIO
import time
import os
import controller as controller_methods
from simple_rest_client.api import API
import simplejson as json

api = API(
  api_root_url=os.getenv('API_IP'), # base api url
  params={}, # default params
  headers={}, # default headers
  timeout=2, # default timeout in seconds
  append_slash=False, # append slash to final url
  json_encode_body=True, # encode body as json
)

api.add_resource(resource_name='controller')

response = api.controller.list()
controllers = {}

for controller in json.loads(response.body):
  controllers[f'{controller["ModuleName"]}-{controller["DeviceTypeName"]}'] = controller['CurrentDeviceGPIO']

def init(pin):
  GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

def run(pin, action):
  GPIO.output(pin, not action)
  return not action

def deinit(pin):
  GPIO.cleanup(pin)
    