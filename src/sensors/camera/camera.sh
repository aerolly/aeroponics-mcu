#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -d /dev/video0 -r 1280x720 --no-banner /home/farmer/aeroponics-mcu/src/sensors/images/camera1_$DATE.jpg
fswebcam -d /dev/video4 -r 1280x720 --no-banner /home/farmer/aeroponics-mcu/src/sensors/images/camera3_$DATE.jpg
fswebcam -d /dev/video2 -r 1280x720 --no-banner /home/farmer/aeroponics-mcu/src/sensors/images/camera2_$DATE.jpg
#fswebcam -d /dev/video5 -r 1280x720 --no-banner /home/farmer/aeroponics-mcu/src/sensors/images/camera4_$DATE.jpg

scp ../images/camera1_$DATE.jpg farmer@192.168.1.28:/home/farmer/images/
scp ../images/camera2_$DATE.jpg farmer@192.168.1.28:/home/farmer/images/
scp ../images/camera3_$DATE.jpg farmer@192.168.1.28:/home/farmer/images/
#scp ../images/camera4_$DATE.jpg farmer@192.168.1.28:/home/farmer/images/
