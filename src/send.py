import redis
import os
import simplejson as json

import settings

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)

test = json.dumps({
  'command': 'sensor',
  'options': {
    'deviceName': 'test',
    'action': 0
  }
})

r.publish('scheduler', test)
