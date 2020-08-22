import redis
import os
import simplejson as json
import time

import settings

r = redis.Redis(host=os.getenv('REDIS_IP'), port=os.getenv('REDIS_PORT'), db=0)

test = json.dumps({
  'command': 'sensor',
  'options': {
    'key': 'temperature',
    'action': 1
  }
})

switch = json.dumps({
  'command': 'controller',
  'options': {
    'key': 'system-pump',
    'action': 0
  }
})

temp = json.dumps({
  'command': 'sensor',
  'options': {
    'key': 'temperature',
  }
})

s = json.dumps({
  'key': 'temperature',
  'result': 12
})

while True:
  r.publish('scheduler', temp)
  time.sleep(10)
