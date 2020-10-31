import time
import os
import requests
import simplejson as json

import settings

sensors = {}

try:
  response = requests.get(f'{os.getenv("API_IP")}/sensor', timeout=2)

  for sensor in json.loads(response.json()):
    sensors[f'{sensor["NodeName"]}-{sensor["ModuleName"]}-{sensor["DeviceTypeName"]}'] = sensor["CurrentDeviceID"]
except requests.exceptions.ConnectionError:
  print('Connection error.')
