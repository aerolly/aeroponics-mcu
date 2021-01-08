import RPi.GPIO as GPIO
import threading
import sys
import traceback
import socket

import settings

from utility.redis_client import r, p

from processes.handleCommand import handleCommand
from processes.handleBackupSchedule import handleBackupSchedule
from processes.handleRedisSchedule import handleRedisSchedule

# Based off of GPIO #
GPIO.setmode(GPIO.BCM)
live = True

# Controller methods
import controller as controller_methods

# Sensor & controller metadata
from sensors import temperature
from resources.controller import controllers

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

  
