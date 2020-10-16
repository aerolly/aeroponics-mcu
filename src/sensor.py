import time
import os
import requests
import simplejson as json

import settings

response = requests.get(f'{os.getenv("API_IP")}/sensor', timeout=2)

sensors = []

for sensor in json.loads(response.body):
  sensors.append(sensor['DeviceTypeName'])
