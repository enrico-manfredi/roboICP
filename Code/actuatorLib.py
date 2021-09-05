import RPi.GPIO as GPIO
from time import sleep 

class actuator:
    def __init__(self):

        self.f = 19
        self.b = 21

        GPIO.setup(self.b, GPIO.OUT)
        GPIO.setup(self.f, GPIO.OUT)

        self.reset()
    
    def reset(self):
        self.backward(30)
    
    def stop(self):
        GPIO.output(self.b,GPIO.LOW)
        GPIO.output(self.f,GPIO.LOW)

    def forward(self,time):
        GPIO.output(self.b,GPIO.LOW)
        GPIO.output(self.f,GPIO.HIGH)

        sleep(time)

        self.stop()

    def backward(self,time):
        GPIO.output(self.f,GPIO.LOW)
        GPIO.output(self.b,GPIO.HIGH)

        sleep(time)

        self.stop()
        
    def pushSyringe(self):
        self.forward(2)
        for i in range(30):
            self.forward(0.1)
            sleep(2)
    
    def getSyringe(self):
        self.forward(15)
        
    def pullSyringe(self):
        self.backward(5)
        
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    ac = actuator()
    ac.push()
    ac.push()
    print("yeee")
    
    
    

    