import RPi.GPIO as GPIO
import time

class servo:
    def __init__(self,pin):
        self.pwm = pin
        
        GPIO.setup(self.pwm, GPIO.OUT)
        self.p = GPIO.PWM(self.pwm, 50)
        self.p.start(2.5)
        
        self.startingPosition()
        
        
    def turn(self,duty):
        print(duty)
        self.p.ChangeDutyCycle(duty)
        


class servoLiquid(servo):
    
    def startingPosition(self):
        self.release()

    def press(self):
        self.turn(7)
        time.sleep(2)

    def release(self):
        self.turn(11)
        time.sleep(2)

class servoTip(servo):
    
    def startingPosition(self):
        self.release()

    def press(self):
        self.turn(7)
        time.sleep(2)

    def release(self):
        self.turn(9)
        time.sleep(2)


class servoLock(servo):
    
    def startingPosition(self):
        self.open()
        

    def open(self):
        self.turn(5)
        time.sleep(2)
    
    def lock(self):
        self.turn(10)
        time.sleep(2)

        
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    s = servoTip(15)
    s.press()
    s.release()
    GPIO.cleanup()
    print("hh")