import time
import os
from simple_rest_client.api import API
import simplejson as json

import settings

api = API(
  api_root_url=os.getenv('API_IP'), # base api url
  params={}, # default params
  headers={}, # default headers
  timeout=2, # default timeout in seconds
  append_slash=False, # append slash to final url
  json_encode_body=True, # encode body as json
)

api.add_resource(resource_name='sensor')

response = api.sensor.list()
sensors = []

for sensor in json.loads(response.body):
  sensors.append(sensor['DeviceTypeName'])
