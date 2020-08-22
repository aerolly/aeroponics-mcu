import RPi.GPIO as GPIO
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
import controller as controller_methods
from sensors import temperature
from controller import controllers

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)

controllerQueue = []
sensorQueue = []

def initializeHardware():
  temperature.init()
  for controller in controllers:
    controller_methods.init(controllers[controller])

def deinitializeHardware():
  # Solid state relay GPIO deinitializations
  for controller in controllers:
    controller_methods.deinit(controllers[controller])

# Process the queue of events and run 
def handleControllerQueue():
  while True:
    if len(controllerQueue) > 0:
      try:
        command = controllerQueue.pop(0)

        print(f'Processing {command}')

        c = Command(command['command'], command['options'])

        out = c.handleCommand()

        r.set(out['key'], out['result'])
        r.publish('data', json.dumps(out))
      except json.JSONDecodeError as error:
        print(error.msg)
    time.sleep(1)

# Process the queue of events and run 
def handleSensorQueue():
  while True:
    if len(sensorQueue) > 0:
      try:
        command = sensorQueue.pop(0)

        print(f'Processing {command}')

        c = Command(command['command'], command['options'])

        out = c.handleCommand()

        r.set(out['key'], out['result'])
        r.publish('data', json.dumps(out))
      except json.JSONDecodeError as error:
        print(error.msg)
    time.sleep(1)

# Parse array of commands to be executed 
# Assume that all items in the array are of the same type
def handleRedisSchedule():
  try:
    p.subscribe('scheduler')
  except:
    print('Could not subscribe')

  while True:
    for message in p.listen():
      try:
        msg = json.loads(message['data'].decode('utf-8'))

        if (msg['command'] == 'controller'):
          controllerQueue.append(msg)
        elif (msg['command'] == 'sensor'):
          sensorQueue.append(msg)

        print(f'Received event {msg["command"]}')
      except json.JSONDecodeError as error:
        print(error.msg) 
      except UnicodeError:
        print('Error decoding Redis message')
    time.sleep(1)

if __name__ == "__main__":
  initializeHardware()
  try:
    controllerThread = threading.Thread(target=handleControllerQueue)
    sensorThread = threading.Thread(target=handleSensorQueue)
    redisPub = threading.Thread(target=handleRedisSchedule)

    print('Starting scheduler')
    controllerThread.start()
    sensorThread.start()
    redisPub.start()  

    controllerThread.join()
    sensorThread.join()
    redisPub.join()
    print('Stopped scheduler')
  except KeyboardInterrupt:

    print("Shutdown requested...exiting")
  except Exception:
    traceback.print_exc(file=sys.stdout)
  finally:
    deinitializeHardware()
    sys.exit(0)

# while True:
  
