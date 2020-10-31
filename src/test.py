import socket
import json
import time
import schedule
import redis
import os
import threading

import settings

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)

live = True

server_address = ('localhost', 20001)

def send_command(message):
  try:
    # Send data
    # if not live:
    sock.sendto(bytes(message, 'utf-8'), server_address)
  finally:
    sock.close()

def sprayLower():
  send_command(json.dumps({
    'command': 'controller',
    'options': {
      'key': 'genesis-lowerBed-solenoid',
      'action': 1,
      'waitTime': 10
    }
  }))

def sprayUpper():
  send_command(json.dumps({
    'command': 'controller',
    'options': {
      'key': 'genesis-upperBed-solenoid',
      'action': 1,
      'waitTime': 10
    }
  }))

def pump():
  send_command(json.dumps({
    'command': 'controller',
    'options': {
      'key': 'genesis-system-pump',
      'action': 1,
      'waitTime': 1
    }
  }))

pump()
