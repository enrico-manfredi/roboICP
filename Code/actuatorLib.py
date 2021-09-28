import RPi.GPIO as GPIO
from time import sleep 

class Actuator:
    def __init__(self):

        self.f = 19 #forwards gpio pin
        self.b = 21 #backwards gpio pin

        #set pinmodes
        GPIO.setup(self.b, GPIO.OUT)
        GPIO.setup(self.f, GPIO.OUT)

        self.reset() #resets the actuator on starting pos on init
    
    def reset(self):
        """reset the actuator to retracted position"""
        self.backward(30) #puts the backwards pin high for 30seconds
        
        ##are there any issues with keeping the motor running backwards when it's
        ##already fully retracted?
    
    def stop(self):
        """stops actuator where it currently is"""
        GPIO.output(self.b,GPIO.LOW)
        GPIO.output(self.f,GPIO.LOW)

    def forward(self,time):
        """"time in seconds to run act forwards for"""
        GPIO.output(self.b,GPIO.LOW) #
        GPIO.output(self.f,GPIO.HIGH)

        sleep(time)

        self.stop()

    def backward(self,time):
        """"time in seconds to run act backwards for"""
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
        
#testing script
#silent on import
if __name__ == '__main__':
    #cycle the actuator as if it was going for a syringe to
    #check everythign is working
    
    ##I assume this is the cycle it will perform?
    
    GPIO.setmode(GPIO.BOARD)
    ac = Actuator()
    ac.reset()
    ac.getSyringe()
    ac.pullSyringe()
    ac.pushSyringe()
    sleep(10)
    ac.pullSyringe()
    ac.reset()
    print("yeee") #confirmation of execution
    
    
    

    
