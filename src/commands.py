from sensors import temperature, pressure
from devices import pump, lowerSolenoid, upperSolenoid

class Command:
  # Initialize command class
  def __init__(self, command, options):
    self.command = command
    self.options = options

  # Decide what to do with command
  def handleCommand(self):
    if (self.command == 'device'):
      self.handleDevice()
    elif (self.command == 'sensor'):
      self.handleSensor()

  # Control device
  def handleDevice(self):
    try:
      getattr(self.options.deviceName, 'run')(self.options.action)
    except AttributeError:
      return str(AttributeError)

  # Get data from sensor
  def handleSensor(self):
    try:
      getattr(self.options.sensorType, 'run')()
    except AttributeError:
      return str(AttributeError)
  