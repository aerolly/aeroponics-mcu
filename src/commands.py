# from sensors import temperature, pressure
import devices

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
      # Dynamically call device name
      name = "devices." + self.options['deviceName']
      mod = __import__(name, fromlist=[''])

      # Run run() function 
      mod.run(self.options['action'])
    except AttributeError:
      print(AttributeError)

  # Get data from sensor
  def handleSensor(self):
    try:
      # Dynamically call sensor name
      name = "sensors." + self.options['deviceName']
      mod = __import__(name, fromlist=[''])

      # Run run() function 
      mod.run()
    except AttributeError:
      print(AttributeError)
  