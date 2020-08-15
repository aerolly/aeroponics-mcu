from dotenv import load_dotenv
import redis
import os

load_dotenv()

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)

while True:

