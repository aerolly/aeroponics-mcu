# from sensors import temperature, pressure
from controller import controllers
from sensor import sensors
from datetime import datetime, timezone
import time
import controller

class Command:
  # Initialize command class
  def __init__(self, command, options):
    self.command = command
    self.options = options

  # Decide what to do with command
  def handleCommand(self):
    if (self.command == 'controller'):
      result = self.handleController()
      return {
        "type": self.command,
        "time": datetime.fromtimestamp(time.time()).replace(tzinfo=timezone.utc).timestamp(),
        "key": self.options['key'],
        "result": result
      }
    elif (self.command == 'sensor'):
      result = self.handleSensor()
      return {
        "type": self.command,
        "time": datetime.fromtimestamp(time.time()).replace(tzinfo=timezone.utc).timestamp(),
        "key": self.options['key'],
        "result": result
      }
    else:
      print('Invalid command type provided.')

  # Control device
  def handleController(self):
    try:
      return controller.run(controllers[self.options['key']] , self.options)
    except AttributeError:
      print(AttributeError)

  # Get data from sensor
  def handleSensor(self):
    try:
      # Dynamically call sensor name
      name = "sensors." + self.options['key']
      mod = __import__(name, fromlist=[''])

      # Run run() function 
      return mod.run()
    except AttributeError:
      print(AttributeError)
  