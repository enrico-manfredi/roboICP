
##what is this meant to test?

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)


print("yes")
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

GPIO.output(3,GPIO.HIGH)

for i in range(5000):
    GPIO.output(5,GPIO.HIGH)
    GPIO.output(5,GPIO.LOW)
    sleep(0.001)
    
print("yeet")
GPIO.cleanup()
