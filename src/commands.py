# from sensors import temperature, pressure
import devices

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
        "key": self.options['deviceName'],
        "result": result
      }
    elif (self.command == 'sensor'):
      result = self.handleSensor()
      return {
        "key": self.options['deviceName'],
        "result": result 
      }
    else:
      print('Invalid command type provided.')

  # Control device
  def handleController(self):
    try:
      # Dynamically call device name
      name = "controllers." + self.options['deviceName']
      mod = __import__(name, fromlist=[''])

      # Run run() function 
      attr = getattr(mod, self.options['deviceName'])

      return attr.run(self.options['action'], self.options['duration'])
    except AttributeError:
      print(AttributeError)

  # Get data from sensor
  def handleSensor(self):
    try:
      # Dynamically call sensor name
      name = "sensors." + self.options['deviceName']
      mod = __import__(name, fromlist=[''])

      # Run run() function 
      attr = getattr(mod, self.options['deviceName'])

      return attr.run()
    except AttributeError:
      print(AttributeError)
  