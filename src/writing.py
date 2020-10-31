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
    if not live:
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
      'waitTime': 60
    }
  }))

schedule.every().day.at("08:03").do(pump)
schedule.every().day.at("12:00").do(pump)

schedule.every().day.at("07:05").do(sprayLower)
schedule.every().day.at("07:20").do(sprayLower)
schedule.every().day.at("07:35").do(sprayLower)
schedule.every().day.at("07:50").do(sprayLower)
schedule.every().day.at("09:05").do(sprayLower)
schedule.every().day.at("09:20").do(sprayLower)
schedule.every().day.at("09:35").do(sprayLower)
schedule.every().day.at("09:50").do(sprayLower)
schedule.every().day.at("10:05").do(sprayLower)
schedule.every().day.at("10:20").do(sprayLower)
schedule.every().day.at("10:35").do(sprayLower)
schedule.every().day.at("10:50").do(sprayLower)
schedule.every().day.at("11:05").do(sprayLower)
schedule.every().day.at("11:20").do(sprayLower)
schedule.every().day.at("11:35").do(sprayLower)
schedule.every().day.at("11:50").do(sprayLower)
schedule.every().day.at("12:05").do(sprayLower)
schedule.every().day.at("12:20").do(sprayLower)
schedule.every().day.at("12:35").do(sprayLower)
schedule.every().day.at("12:50").do(sprayLower)
schedule.every().day.at("13:05").do(sprayLower)
schedule.every().day.at("13:20").do(sprayLower)
schedule.every().day.at("13:35").do(sprayLower)
schedule.every().day.at("13:50").do(sprayLower)
schedule.every().day.at("14:05").do(sprayLower)
schedule.every().day.at("14:20").do(sprayLower)
schedule.every().day.at("14:35").do(sprayLower)
schedule.every().day.at("14:50").do(sprayLower)
schedule.every().day.at("15:05").do(sprayLower)
schedule.every().day.at("15:20").do(sprayLower)
schedule.every().day.at("15:35").do(sprayLower)
schedule.every().day.at("15:50").do(sprayLower)
schedule.every().day.at("16:05").do(sprayLower)
schedule.every().day.at("16:20").do(sprayLower)
schedule.every().day.at("16:35").do(sprayLower)
schedule.every().day.at("16:50").do(sprayLower)
schedule.every().day.at("17:05").do(sprayLower)
schedule.every().day.at("17:20").do(sprayLower)
schedule.every().day.at("17:35").do(sprayLower)
schedule.every().day.at("17:50").do(sprayLower)
schedule.every().day.at("00:00").do(sprayLower)

schedule.every().day.at("07:00").do(sprayUpper)
schedule.every().day.at("07:15").do(sprayUpper)
schedule.every().day.at("07:30").do(sprayUpper)
schedule.every().day.at("07:45").do(sprayUpper)
schedule.every().day.at("08:00").do(sprayUpper)
schedule.every().day.at("08:15").do(sprayUpper)
schedule.every().day.at("08:30").do(sprayUpper)
schedule.every().day.at("08:45").do(sprayUpper)
schedule.every().day.at("09:00").do(sprayUpper)
schedule.every().day.at("09:15").do(sprayUpper)
schedule.every().day.at("09:30").do(sprayUpper)
schedule.every().day.at("09:45").do(sprayUpper)
schedule.every().day.at("10:00").do(sprayUpper)
schedule.every().day.at("10:15").do(sprayUpper)
schedule.every().day.at("10:30").do(sprayUpper)
schedule.every().day.at("10:45").do(sprayUpper)
schedule.every().day.at("11:00").do(sprayUpper)
schedule.every().day.at("11:15").do(sprayUpper)
schedule.every().day.at("11:30").do(sprayUpper)
schedule.every().day.at("11:45").do(sprayUpper)
schedule.every().day.at("12:03").do(sprayUpper)
schedule.every().day.at("12:15").do(sprayUpper)
schedule.every().day.at("12:30").do(sprayUpper)
schedule.every().day.at("12:45").do(sprayUpper)
schedule.every().day.at("13:00").do(sprayUpper)
schedule.every().day.at("13:15").do(sprayUpper)
schedule.every().day.at("13:30").do(sprayUpper)
schedule.every().day.at("13:45").do(sprayUpper)
schedule.every().day.at("14:00").do(sprayUpper)
schedule.every().day.at("14:15").do(sprayUpper)
schedule.every().day.at("14:30").do(sprayUpper)
schedule.every().day.at("14:45").do(sprayUpper)
schedule.every().day.at("15:00").do(sprayUpper)
schedule.every().day.at("15:15").do(sprayUpper)
schedule.every().day.at("15:30").do(sprayUpper)
schedule.every().day.at("15:45").do(sprayUpper)
schedule.every().day.at("16:00").do(sprayUpper)
schedule.every().day.at("16:15").do(sprayUpper)
schedule.every().day.at("16:30").do(sprayUpper)
schedule.every().day.at("16:45").do(sprayUpper)
schedule.every().day.at("17:00").do(sprayUpper)
schedule.every().day.at("17:15").do(sprayUpper)
schedule.every().day.at("17:30").do(sprayUpper)
schedule.every().day.at("17:45").do(sprayUpper)
schedule.every().day.at("00:05").do(sprayLower)

def sched():
  while True:
    schedule.run_pending()
    time.sleep(1)

def redisConnection():
  while True:
    try:
      r.ping()
      live = True
    except:
      live = False
    time.sleep(5)

if __name__ == "__main__":
  scheduler = threading.Thread(target=sched)
  redisConnection = threading.Thread(target=redisConnection)

  scheduler.start()
  redisConnection.start()

  scheduler.join()
  redisConnection.join()
