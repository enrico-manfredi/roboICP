import RPi.GPIO as GPIO
from time import sleep

class linearRail:

    def __init__(self):
        
        self.direction = 11
        self.pulse = 13

        GPIO.setup(self.direction, GPIO.OUT)
        GPIO.setup(self.pulse, GPIO.OUT)

        GPIO.output(self.direction,GPIO.HIGH)

        self.position = 0
        self.steps_per_syringe = 50000
        self.first_pos = 3600 * 5

        self.calibrate()

    def calibrate(self):
        self.backward()
        self.move(200000)

    def backward(self):
        GPIO.output(self.direction,GPIO.LOW)
    
    def forward(self):
        GPIO.output(self.direction,GPIO.HIGH)

    def moveToSyringe(self,n_syringe):
        syringe_step_pos = (self.steps_per_syringe * n_syringe) + (self.first_pos)
        steps_to_move = syringe_step_pos - self.position
        self.moveToPos(steps_to_move)

    def moveToPos(self,pos):
        if pos < self.position:
            self.backward()
        else: 
            self.forward()

        self.move(abs(pos-self.position))

        self.position = pos
        
    def move(self,n_of_pulses):
        for i in range(n_of_pulses):
            GPIO.output(self.pulse,GPIO.HIGH)
            GPIO.output(self.pulse,GPIO.LOW)
            sleep(0.001)

    def reset(self):
        GPIO.output(self.direction,GPIO.LOW)
        self.move(self.position)
        GPIO.output(self.direction,GPIO.HIGH)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    li = linearRail()
    sleep(5)
    for syringe in range(5):
        print("yee")
        li.moveToSyringe(syringe)
        sleep(5)
    GPIO.cleanup()