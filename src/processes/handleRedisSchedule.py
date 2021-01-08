import concurrent.futures
import simplejson as json
import time
import redis

from utility.redis_client import r, p

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
        print('Redis connection timed out')
      except redis.exceptions.TimeoutError:
        print('Redis connection timed out')
      except:
        print('error')
