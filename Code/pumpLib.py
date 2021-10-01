import RPi.GPIO as GPIO
from time import sleep 

class acidPump:
    def __init__(self):
        """Pump class currently calibrated to do 1ml per second"""
        self.f = 33
        self.b = 35
        self.pwm = 37

        GPIO.setup(self.b, GPIO.OUT)
        GPIO.setup(self.f, GPIO.OUT)
        GPIO.setup(self.pwm, GPIO.OUT)
        self.p = GPIO.PWM(self.pwm, 50)
        self.p.start(2.5)
        
        self.p.ChangeDutyCycle(46)#46-> 1ml per second dispense rate
        
        self.stop()
        
    def calibrate(self):
         """runs the acid through all the pipe to get rid of air bubbles"""
        self.dispense(40)
        
    
    def stop(self):
        GPIO.output(self.b,GPIO.LOW)
        GPIO.output(self.f,GPIO.LOW)

    def dispense(self,ml):
        GPIO.output(self.b,GPIO.LOW)
        GPIO.output(self.f,GPIO.HIGH)

        sleep(ml)

        self.stop()
        
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    p = acidPump()
    p.dispense(6)
    
    

    
