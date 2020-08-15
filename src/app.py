import RPi.GPIO as GPIO
from dotenv import load_dotenv
import redis
import os
import time
import threading
import simplejson as json

load_dotenv()

from commands import Command

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)

scheduleQueue = []

def initializeHardware():
  # Temperature sensor mounting
  os.system('modprobe w1-gpio')
  os.system('modprobe w1-therm')

  # Solid state relay GPIO initializations
  GPIO.setmode(GPIO.BCM)

  pins = [17, 27, 22]
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

def deinitializeHardware():
  # Solid state relay GPIO deinitializations
  GPIO.cleanup([17, 27, 22])

# Process the queue of events and run 
def handleQueue():
  while True:
    if len(scheduleQueue) > 0:
      try:
        command = json.loads(scheduleQueue.pop(0))

        c = Command(command.command, command.options)

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
    print('test out')
    for message in p.listen():
      scheduleQueue.append(message)
    time.sleep(1)

if __name__ == "__main__":
  queue = threading.Thread(target=handleQueue)
  redisPub = threading.Thread(target=handleRedisSchedule)

  print('Starting scheduler')
  queue.start()
  redisPub.start()  

  print('Stopping scheduler')
  queue.join()
  redisPub.join()
# while True:
  
