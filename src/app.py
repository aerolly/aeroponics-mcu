import RPi.GPIO as GPIO
import redis
import os
import time
import threading
import simplejson as json
import sys
import traceback

import settings
from commands import Command
from sensors.temperature import initializeTemperature

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)

scheduleQueue = []

def initializeGPIO():
  # Solid state relay GPIO initializations
  GPIO.setmode(GPIO.BCM)

  pins = [17, 27, 22]
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH) # off (negative logic)

def initializeHardware():
  initializeTemperature()
  initializeGPIO()

def deinitializeHardware():
  # Solid state relay GPIO deinitializations
  GPIO.cleanup([17, 27, 22])

# Process the queue of events and run 
def handleQueue():
  while True:
    if len(scheduleQueue) > 0:
      try:
        command = json.loads(scheduleQueue.pop(0))

        print(f'Processing {command}')

        c = Command(command['command'], command['options'])

        c.handleCommand()
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
    initializeHardware()
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

  deinitializeHardware()
  sys.exit(0)
# while True:
  
