import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [17, 27, 22]

GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)

i = 0

while True:
  print('High')
  GPIO.output(17, 1)
  GPIO.output(27, 1)
  GPIO.output(22, 1)
  time.sleep(3)

  print('Low')
  GPIO.output(17, 0)
  GPIO.output(27, 0)
  GPIO.output(22, 0)
  time.sleep(3)

GPIO.cleanup([17, 27, 22])
