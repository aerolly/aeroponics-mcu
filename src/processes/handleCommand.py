# Command handler
from utility.commands import Command

from utility.redis_client import r

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
  except redis.exceptions.TimeoutError:
    print('Redis connection timed out')
  except redis.exceptions.ConnectionError:
    print('Could not establish Redis connection')
  except Exception as e:
    print(e)
