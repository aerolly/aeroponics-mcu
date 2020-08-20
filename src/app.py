import RPi.GPIO as GPIO
from simple_rest_client.api import API
import simplejson as json
import redis
import os
import time
import threading
import sys
import traceback
import time
import settings

GPIO.setmode(GPIO.BCM)

from commands import Command
from sensors.temperature import Temperature
import controller as controller_methods

api = API(
  api_root_url=os.getenv('API_IP'), # base api url
  params={}, # default params
  headers={}, # default headers
  timeout=2, # default timeout in seconds
  append_slash=False, # append slash to final url
  json_encode_body=True, # encode body as json
)

api.add_resource(resource_name='controller')

response = api.controllers.list()
controllers = {}

for controller in response.body:
  print(controller)
  controllers[controller.ModuleName] = controller.CurrentDeviceGPIO

print(controllers)

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)

scheduleQueue = []

def initializeHardware():
  for controller in controllers:
    controller_methods.init(controllers[controller])

def deinitializeHardware(lowerSolenoid, pump, upperSolenoid):
  # Solid state relay GPIO deinitializations
  for controller in controllers:
    controller_methods.deinit(controllers[controller])

# Process the queue of events and run 
def handleQueue():
  while True:
    if len(scheduleQueue) > 0:
      try:
        command = json.loads(scheduleQueue.pop(0))

        print(f'Processing {command}')

        c = Command(command['command'], command['options'])

        out = c.handleCommand()

        r.publish('data', json.dumps(out))
      except json.JSONDecodeError as error:
        print(error.msg)
    time.sleep(1)

def handleRedisSchedule():
  try:
    p.subscribe('scheduler')
  except:
    print('Could not subscribe')

  while True:
    for message in p.listen():
      try:
        msg = message['data'].decode('utf-8')
        scheduleQueue.append(msg)

        print('Received event.')
      except UnicodeError:
        print('Error decoding Redis message')
    time.sleep(1)

if __name__ == "__main__":
  try:
    queue = threading.Thread(target=handleQueue)
    redisPub = threading.Thread(target=handleRedisSchedule)

    print('Starting scheduler')
    queue.start()
    redisPub.start()  

    queue.join()
    redisPub.join()
    print('Stopped scheduler')
  except KeyboardInterrupt:

    print("Shutdown requested...exiting")
  except Exception:
    traceback.print_exc(file=sys.stdout)
  finally:
    deinitializeHardware(lowerSolenoid, pump, upperSolenoid)
    sys.exit(0)

# while True:
  
