import time
import os
import requests
import simplejson as json

import settings

"""Retrieve all sensor metadata from the database and save it to a file for later use.
Store sensors being used in the runtime in memory in the sensors dictionary.
"""

sensors = {}

try:
  # Get current sensors
  response = requests.get(f'{os.getenv("API_IP")}/sensor', timeout=2)

  # Insert into sensors variable
  for sensor in json.loads(response.json()):
    sensors[f'{sensor["NodeName"]}-{sensor["ModuleName"]}-{sensor["DeviceTypeName"]}'] = sensor["CurrentDeviceID"]

  # Save updated list to json file
  f = open('sensors.json', 'w')
  f.write(json.dumps(sensors))
  f.close()
except requests.exceptions.ConnectionError:
  print('Connection error.')
  f = open('sensors.json', 'r')
  controllers = json.loads(f.read())
  f.close()