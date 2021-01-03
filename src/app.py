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

# Based off of GPIO #
GPIO.setmode(GPIO.BCM)
live = True

# Command hndler
from commands import Command

# Controller methods
import controller as controller_methods

# Sensor & controller metadata
from sensors import temperature
from controller import controllers

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)

controllerQueue = []
sensorQueue = []

def initializeHardware():
  """Initialize hardware (e.g. sensors) for use.
  """

  # Initialize one-wire temperature sensor
  temperature.init()

  # Initialize GPIO pins
  for controller in controllers:
    controller_methods.init(controllers[controller])


def deinitializeHardware():
  """Deinitialize hardware for shutdown.
  """

  # De-initialize GPIO pins
  for controller in controllers:
    controller_methods.deinit(controllers[controller])

# Process the queue of events and run
def handleCommand(command):
  """Process an incoming command from the redis pubsub command queue.
  
  Parameters:
  command - standard command packet structure
  """
  try:
    print(f'Processing {command}')

    # Send command and its options to the command class in commands.py
    c = Command(command['command'], command['options'])

    # Run corresponding handle command function
    out = c.handleCommand()
    print(out)

    # Send result of the command to redis key value store
    r.set(out['key'], out['result'])

    # Send result of command over redis pubsub
    r.publish('data', json.dumps(out))
  except json.JSONDecodeError as error:
    print(error.msg)

def handleRedisSchedule():
  """Parse command packet, create thread to process command.
  """
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
  """Backup schedule using UDP. Listens to backup process writing.py if redis disconnects.
  """
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
    redis = threading.Thread(target=handleRedisSchedule)
    backup = threading.Thread(target=handleBackupSchedule)

    redis.start()
    backup.start()

    redis.join()
    backup.join()
    print('Stopped scheduler')
  except Exception:
    traceback.print_exc(file=sys.stdout)
  finally:
    deinitializeHardware()
    sys.exit(0)

  
