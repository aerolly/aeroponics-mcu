# from sensors import temperature, pressure
from controller import controllers
from sensor import sensors
from datetime import datetime, timezone
import time
import controller
import requests
import os

class Command:
  # Initialize command class
  def __init__(self, command, options):
    # Command data (id, type)
    self.command = command

    # Options for the command
    self.options = options

  # Decide what to do with command
  def handleCommand(self):
    """Offload the appropriate processing function based on command type (controller or sensor).

    Returns:
    Packet containing type of command, device ID, time, and result of the command.
    """
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

  def handleController(self):
    """Change the state of a controller.

    Returns:
    The controller state that it was changed to become.
    """
    try:
      # Run the controller run function to modify the GPIO pin logic
      return controller.run(controllers[self.options['key']] , self.options)
    except AttributeError:
      print(AttributeError)

  def handleSensor(self):
    """Sample a sensor and retrieve the value.

    Returns:
    The sampled sensor data point.
    """
    try:
      # Dynamically call sensor by type from the unique ID
      name = "sensors." + self.options['key'].split('-')[2]

      # Get the run function from the corresponding sensor definition in sensors/
      mod = __import__(name, fromlist=[''])
      reading = mod.run()

      # Send sensor result and send it to the API to save to the database
      requests.post(f'{os.getenv("API_IP")}/sensor', timeout=2, json={'id': sensors[self.options['key']], 'reading': reading})

      # Run run() function (result of the sensor reading)
      return reading
    except AttributeError:
      print(AttributeError)
  