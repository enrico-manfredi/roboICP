import RPi.GPIO as GPIO
from time import sleep

class rotationVial:

    def __init__(self):

        self.direction = 3
        self.pulse = 5

        GPIO.setup(self.direction, GPIO.OUT)
        GPIO.setup(self.pulse, GPIO.OUT)

        self.steps = 200 * 16
        self.position = 0

        number_of_vials = 5

        angle_to_turn = 360/number_of_vials
        self.steps_per_vial = (self.steps / 360) * angle_to_turn
        
        self.backward()
    
    def backward(self):
        GPIO.output(self.direction,GPIO.LOW)
    
    def forward(self):
        GPIO.output(self.direction,GPIO.HIGH)
        
    def moveToPos(self,pos):
        print(pos)
        if pos < self.position:
            self.backward()
        else: 
            self.forward()

        self.move(abs(pos-self.position))

        self.position = pos
        
    def move(self,n_of_pulses):
        print("===", n_of_pulses)
        for i in range(int(n_of_pulses)):
            GPIO.output(self.pulse,GPIO.HIGH)
            GPIO.output(self.pulse,GPIO.LOW)
            sleep(0.001)

    def moveToVial(self):
        self.move(1088 * 2 - 300)
    
    def moveToVialFilling(self):
        self.move(1088)
        
    def nextVial(self):
        self.move(236)
        self.move(self.steps_per_vial)

    def reset(self):
        self.moveToPos(0)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    ro = rotationVial()
    s = ro.steps_per_vial
    
    for vials in range(1):
        ro.moveToVialFilling()
        sleep(2)
        ro.moveToVial()
##    for vials in range(5):
##        ro.moveToVial(vials)
##        sleep(5)
        
    ro.reset()

    print("yeet")
    GPIO.cleanup()