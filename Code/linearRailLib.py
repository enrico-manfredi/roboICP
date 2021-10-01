import RPi.GPIO as GPIO
from time import sleep

class LinearRail:

    def __init__(self):
        
        self.direction = 11 #gpio pin that determines direction of slide movement
        self.pulse = 13 #gpio pin that moves the slide when high

        GPIO.setup(self.direction, GPIO.OUT)
        GPIO.setup(self.pulse, GPIO.OUT)

        GPIO.output(self.direction,GPIO.HIGH) #default direction is forward

        #TODO calibrate the two variables below:  steps_per_syringe-> number of steps to move from one syringe to another
        # first_pos -> number of steps required to align the first syringe with the piston head
        self.steps_per_syringe = 50000 #note: steps are absolute not relative
        self.first_pos = 3600 * 5 ##what does this refer to? first syringe pos?
        
        ##how long is each step in mm?

        self.calibrate()

        self.position = 0

    def calibrate(self):
        self.backward()
        self.move(200000)
        
        ##there is no backrun protection for the linear rail so it grinds itself out
        ##need to add a limit switch instead of just having it bash on the end
        ##probably some additional circuitry required to add an interrupt signal

    def backward(self):
        GPIO.output(self.direction,GPIO.LOW) #backward is low
    
    def forward(self):
        GPIO.output(self.direction,GPIO.HIGH) #forward is high

    def moveToSyringe(self,n_syringe):
        """enter syringe # to dispense between 0-4 with 0 being the first"""
        #self.firstpos is the first syringe and takes care of n=0 case
        syringe_step_pos = (self.steps_per_syringe * n_syringe) + (self.first_pos)
        steps_to_move = syringe_step_pos - self.position
        self.moveToPos(steps_to_move)

    def moveToPos(self,pos):
        """moves rail to specified position in steps (int)"""
        #if the number of steps to targ is less than current pos, go back
        if pos < self.position:
            self.backward()
        #if the number of steps to targ is greater than current pos, go forward
        else: 
            self.forward()

        self.move(abs(pos-self.position)) #determines how far to move by taking absolute diff
        #direction to move is set above

        self.position = pos #updates position with targ once move is finished
        
    def move(self,n_of_pulses):
        """moves stepper by one pulse (step)"""
        for i in range(n_of_pulses):
            GPIO.output(self.pulse,GPIO.HIGH)
            GPIO.output(self.pulse,GPIO.LOW)
            sleep(0.001) #reset time for next pulse

    def reset(self):
        """switches to backwards direction and moves\
        same number of steps back as current position"""
        GPIO.output(self.direction,GPIO.LOW)
        self.move(self.position)
        GPIO.output(self.direction,GPIO.HIGH)

#unit test - silent on import
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    li = LinearRail()
    sleep(5)
    for syringe in range(5):
        print("yee")
        li.moveToSyringe(syringe)
        sleep(5)
    GPIO.cleanup()
