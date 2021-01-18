import socket
import json
import time
from datetime import datetime 
import os
import threading
import concurrent.futures
import schedule
import scheduler_utility as su

import settings

###########################
# Automatically run jobs generated from database
###########################

# Set time between refreshes
secondsBetweenReload = 86400
# Threads die when refreshInd = 1
refreshInd = 0


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20001)


# Load scheduled jobs into memory
scheduledJobs = None


def send_command(job):
  message = json.dumps({
    'command': 'controller',
    'options': {
      'key': f"{job['NodeName']}-{job['ModuleName']}-{job['DeviceTypeName']}",
      'action': 1,
      'waitTime': job['SchedulerSecondsToKeepActive']
    }
  })
  print(message)
  sock.sendto(bytes(message, 'utf-8'), server_address)


# Update scheduler jobs 
def scheduler_sync():
  global refreshInd 
  global scheduledJobs

  refreshInd = 1
  su.saveSchedule()
  scheduledJobs = su.getSchedule()
  time.sleep(secondsBetweenReload)


def handleSchedulerJob(job):
  # preprocessing
  print('entered job handler')
  startTime = datetime.strptime(job['SchedulerDailyStartTime'],'%H:%M:%S').time()
  endTime = datetime.strptime(job['SchedulerDailyStopTime'],'%H:%M:%S').time()

  # wait until job start time
  while startTime > datetime.now().time():
    if refreshInd == 1: # end thread if jobs are being refreshed
      return
    time.sleep(5)
  
  # Time based activation
  if job['SchedulerActivateOnMinValue'] is None:
    minuteWait = job['SchedulerMinutesBetweenActivation']
    print(f'scheduling every {minuteWait} minutes')
    print(f'job: \n{job}')

    schedule.every(minuteWait).minutes.do(send_command, job=job).tag(job['ScheduleID'])
    # Remove scheduled jobs after job expires
    while refreshInd != 1 and endTime > datetime.now().time():
      time.sleep(5)
    schedule.clear(tag=job['ScheduleID'])
    return
  # Activate on lower value of sensor
  elif job['SchedulerActivateOnMinValue'] is True:
    print('not implemented')
  # Activate on higher value of sensor
  else:
    print('not implemented')


def sched():
  global refreshInd
  while True:
    # don't run if no jobs
    while scheduledJobs is None:
      print('waiting for jobs')
      time.sleep(5)
    # Threads run until stoptime, or refreshInd = 1
    refreshInd = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = []
      for job in scheduledJobs:
        futures.append(executor.submit(handleSchedulerJob, job))
      for future in futures:
        future.result()


# Run pending schedule jobs
def runSched():
  while True:
    schedule.run_pending()
    time.sleep(5)
      

if __name__ == "__main__":
  print('Starting schedule')
  sync = threading.Thread(target=scheduler_sync)
  scheduler = threading.Thread(target=sched)
  executor = threading.Thread(target=runSched)

  sync.start()
  scheduler.start()
  executor.start()

  sync.join()
  scheduler.join()
  executor.join()