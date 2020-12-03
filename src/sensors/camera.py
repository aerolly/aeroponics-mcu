import os
import datetime
import sys
import time
import subprocess


def run(param):
    currentDateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

    destUser = os.getenv('SERVER_USER')
    destIP = os.getenv('REDIS_SERVER')
    imageName = f'{param}_{currentDateTime}.jpg'
    localDestPath = f'/home/{destUser}/aeroponics-mcu/src/sensors/images/{imageName}'
    remoteDestPath = f'/home/{destUser}/images/'
    cameraPath = f'/dev/{param}'

    takePic = f'fswebcam -d {cameraPath} -r 1280x720 --no-banner {localDestPath}'

    os.system(takePic)
    os.system(f'scp {localDestPath} {destUser}@{destIP}:{remoteDestPath}')

    return f'{remoteDestPath}{imageName}'
