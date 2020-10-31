import RPi.GPIO as GPIO
import simplejson as json
import concurrent.futures
import redis
import os
import time
import threading
import sys
import traceback
import time
import settings
import socket

GPIO.setmode(GPIO.BCM)
live = True

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
def handleCommand(command):
  try:
    print(f'Processing {command}')

    c = Command(command['command'], command['options'])

    out = c.handleCommand()
    print(out)

    r.set(out['key'], out['result'])
    r.publish('data', json.dumps(out))
  except json.JSONDecodeError as error:
    print(error.msg)

# Parse array of commands to be executed 
# Assume that all items in the array are of the same type
def handleRedisSchedule():
  try:
    p.subscribe('scheduler')
  except:
    print('Could not subscribe')

  with concurrent.futures.ThreadPoolExecutor() as executor:
    while True:
      try:
        for message in p.listen():
          try:
            msg = json.loads(message['data'].decode('utf-8'))

            executor.submit(handleCommand, msg)
            time.sleep(1)

            print(f'Received event {msg["command"]}')
          except json.JSONDecodeError as error:
            print(error.msg) 
          except UnicodeError:
            print('Error decoding Redis message')
          except KeyboardInterrupt:
            print("Shutdown requested...exiting")
            return
      except redis.exceptions.ConnectionError:
        live = False
      except:
        live = False

def handleBackupSchedule():
  localIP = "127.0.0.1"
  localPort = 20001
  bufferSize = 1024

  # Create a datagram socket
  UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

  # Bind to address and ip
  UDPServerSocket.bind((localIP, localPort))
  
  # Listen for incoming datagrams
  while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    with concurrent.futures.ThreadPoolExecutor() as executor:
      msg = json.loads(message.decode('utf-8'))
      executor.submit(handleCommand, msg)
      time.sleep(1)

if __name__ == "__main__":
  initializeHardware()
  try:
    print('Starting scheduler')
    redis = threading.Thread(handleRedisSchedule)
    backup = threading.Thread(handleBackupSchedule)

    redis.join()
    backup.join()
    print('Stopped scheduler')
  except Exception:
    traceback.print_exc(file=sys.stdout)
  finally:
    deinitializeHardware()
    sys.exit(0)

  
