from serial import Serial
import time


class printer:

    def __init__(self):
        self.ser = Serial('/dev/ttyACM1', 115200)
        # Note: After each use of send make sure the command is finished before 
        # sending the next Gcode command
        
        # Calibrate the bottom 5 variables depending on coordiates
        self.vialPickupPos = [70,103,6]
        self.tipPickupPos = [51,103,6]
        self.vialDropoffPos = [[25,50,40], 
                                [45,50,40], 
                                [75,50,40], 
                                [95,50,40], 
                                [95,74,40]]
        self.vialAcidDropoffPos = [[0,31,0], 
                                [25,31,0], 
                                [51,31,0], 
                                [73,31,0], 
                                [73,61,0]]
        
        self.dumpPos = [0,70,48]

        time.sleep(2)
        self.home()
        self.acidSetup()

    def send(self,Gcode):
        """Sends the Gcode to printer in the corrent format"""
        self.ser.write(str.encode(Gcode))

    def home(self):
        """Calibration of the printer makes sure everything is at (0,0,0)"""
        print("Homeing....")
        self.send("G28 \n")
        time.sleep(20)
        print("FINISHED Homeing....")
        
    def vialLiqiudPickup(self):
        """moves to saftey height and then goes to liquid pickup location"""
        self.moveZ(48)

        self.moveX(self.vialPickupPos[0])
        time.sleep(3)
        self.moveY(self.vialPickupPos[1])
        time.sleep(3)
        self.moveZ(self.vialPickupPos[2])
        time.sleep(3)

        self.moveZ(6)


    
    def pippeteTipPickup(self):
        """moves to saftey height and then goes to pippete tip pickup location"""
        self.moveZ(40)

        self.moveX(self.tipPickupPos[0])
        time.sleep(1)
        self.moveY(self.tipPickupPos[1])
        time.sleep(1)
        self.moveZ(self.tipPickupPos[2])
        time.sleep(1)

    def vialLiquidDispense(self,number):
        self.moveZ(48)

        self.moveX(self.vialDropoffPos[number][0])
        time.sleep(1)
        self.moveY(self.vialDropoffPos[number][1])
        time.sleep(1)
        self.moveZ(self.vialDropoffPos[number][2])
        time.sleep(1)

        time.sleep(10)

    def acidDispence(self,number):
        self.moveZ(40)

        self.moveX(self.vialAcidDropoffPos[number][0])
        time.sleep(1)
        self.moveY(self.vialAcidDropoffPos[number][1])
        time.sleep(1)
        self.moveZ(self.vialAcidDropoffPos[number][2])
        time.sleep(1)


    def acidSetup(self):
        """moves to dump location"""
        self.dump()

    def moveX(self,coord):
        self.send("G1 X"+ str(coord) + " \r \n")

    def moveY(self,coord):
        self.send("G1 Y"+ str(coord) + " \r \n")

    def moveZ(self,coord):
        self.send("G1 Z"+ str(coord) + " \r \n")
        time.sleep(10)
    
    def dump(self):
        """moves to dump location"""
        self.moveZ(self.dumpPos[2])
        time.sleep(20)
        self.moveY(self.dumpPos[1])
        time.sleep(5)
        self.moveX(self.dumpPos[0])
        time.sleep(5)
        self.moveZ(0)
        time.sleep(20)

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    printer = printer()
    
    for i in range(5):
        print("picking ouo tip")
        printer.pippeteTipPickup()
        time.sleep(30)
        print("liquid pick up")
        printer.vialLiqiudPickup()
        time.sleep(30)
        print("dispensing pick up")
        printer.vialLiquidDispense(i)
        time.sleep(30)
        print("acid dispence pick up")
        printer.acidDispence(i)
        time.sleep(20)

    