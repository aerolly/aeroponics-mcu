import time
import os
import requests
import simplejson as json

import settings

error = 1

try:
  response = requests.get(f'{os.getenv("API_IP")}/sensor', timeout=2)
except requests.exceptions.ConnectionError:
  print('Connection error.')
  error = 0

sensors = {}

for sensor in json.loads(response.json()):
  sensors[f'{sensor["NodeName"]}-{sensor["ModuleName"]}-{sensor["DeviceTypeName"]}'] = sensor["CurrentDeviceID"]
