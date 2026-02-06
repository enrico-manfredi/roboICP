from serial import Serial
from time import sleep


class Printer:

    def __init__(self, port, system):
        """initialise monoprice s mini on port
        -set system to 1 for dilution system (with assoc coordinates)
        -set system to 0 for reaction system (with assoc coordinates)"""
        
        self.open(port)
        #self.send("G1 Z 65 ; \n")
        self.home(wait = False)
        self.ser.close()
        sleep(1)
        self.open(port)
        #self.send("G1 Z 65 ; \n")
        self.system = system
        self.xy_speed = 20 #in mm/s
        self.z_speed = 1.4 #in mm/s

        #dilution system coords
        if self.system == 1:
            self.has_tip = False
            self.vialPickupPos = [5.7, 21.7, 21]
            self.tipPickupPos = [50.3, 88.2, 12.6]
            self.vialDropoffPos = [[72, 48, 15],\
                                   [86, 67, 15],\
                                   [71, 84, 15],\
                                   [62, 104, 15],\
                                   [86, 101, 15]]
            #4th element == 1 indicates half turn
            self.vialAcidDropoffPos = [[38.4, 21.8, 0, 0],\
                                       [52.4, 40.7, 0, 1],\
                                       [41, 57.4, 0, 1],\
                                       [29, 79.4, 19.5, 0],\
                                       [54, 75.4, 0, 0]]
            
            self.dumpPos = [50, 0, 63]
            self.pump_dump = [90, 0, 0]
        
        elif self.system == 0:
            self.stir_pos =  [[61.2, 4.2, 0],\
                             [98.1, 5.2, 0],\
                             [20.9, 90.3, 0],\
                             [58.4, 91.2, 0],\
                             [95, 91.8, 0]]
            
            self.solids_disp = [[0, 14, 4],\
                                [0, 27, 4],\
                                [0, 114, 4],\
                                [0, 100, 4],\
                                [0, 114, 4]]

        #self.prev_pos=[0,0,0] #uncomment when homing is skipped
        self.home()

    #general methods
    def send(self,Gcode):
        self.ser.write(str.encode(Gcode))

    def home(self, wait = True):
        print("Homeing....")
        self.send("G28 ; \r")
        if wait:
            if self.system == 1:
                sleep(25)
            sleep(20)
            self.prev_pos = [0,0,0]

    def close(self):
        self.go_up()
        self.send("M18 ; \n")
        self.ser.close()
        
    def open(self, port):
        self.ser = Serial(port, 115200)
        sleep(15)
        
    def go_up(self):
        """raises z to maximum height to clear obstacles"""
        if self.system == 1:
            if self.has_tip:
                self.moveZ(63)
            else:
                self.moveZ(32.6)
        elif self.system == 0:
            self.moveZ(4)

    def moveX(self,coord):
        t_move = abs(coord - self.prev_pos[0])/self.xy_speed
        self.send("G1 X"+ str(coord) + " ; \n")
        print("moving x to "+str(coord))
        self.prev_pos[0] = coord
        sleep(t_move+1)

    def moveY(self,coord):
        t_move = abs(coord - self.prev_pos[1])/self.xy_speed
        self.send("G1 Y"+ str(coord) + " ; \n")
        print("moving y to "+str(coord))
        self.prev_pos[1] = coord
        sleep(t_move+1)

    def moveZ(self,coord):
        t_move = abs(coord - self.prev_pos[2])/self.z_speed
        self.send("G1 Z"+ str(coord) + " ; \n")
        print("moving z to "+str(coord))
        self.prev_pos[2] = coord
        sleep(t_move+1)

    #dilution system methods
    def vialLiqiudPickup(self):
        self.go_up()
        self.moveX(60) #stop the head from brushing other tips
        self.moveY(self.vialPickupPos[1])
        self.moveX(self.vialPickupPos[0])
        self.moveZ(self.vialPickupPos[2])

    def pippeteTipPickup(self):
        self.go_up()
        self.moveX(self.tipPickupPos[0])
        self.moveY(self.tipPickupPos[1])
        self.moveZ(self.tipPickupPos[2])
        self.has_tip = True

    def vialLiquidDispense(self,number):
        self.go_up()
        self.moveX(self.vialDropoffPos[number][0])
        self.moveY(self.vialDropoffPos[number][1])
        self.moveZ(self.vialDropoffPos[number][2])

    def acidDispense(self,number):
        self.go_up()
        self.moveX(self.vialAcidDropoffPos[number][0])
        self.moveY(self.vialAcidDropoffPos[number][1])
        self.moveZ(self.vialAcidDropoffPos[number][2])


    def acidSetup(self):
        self.go_up()
        self.moveX(self.pump_dump[0])
        self.moveY(self.pump_dump[1])
        self.moveZ(self.pump_dump[2])
    
    def dump(self):
        self.go_up()
        self.moveY(self.dumpPos[1])
        self.moveX(self.dumpPos[0])
        self.moveZ(self.dumpPos[2])
        self.has_tip = False

    #reaction system methods
    def solidsDispense(self, pos):
        self.go_up()
        self.moveX(self.solids_disp[pos][0])
        self.moveY(self.solids_disp[pos][1])
        self.moveZ(self.solids_disp[pos][2])
        
    def solidsPrime(self):
        self.go_up()
        self.moveX(self.solids_disp[1][0])
        self.moveY(self.solids_disp[1][1])
        self.moveZ(self.solids_disp[1][2])
        
    
    def stir(self, pos):
        self.go_up()
        self.moveX(self.stir_pos[pos][0])
        self.moveY(self.stir_pos[pos][1])
        self.moveZ(self.stir_pos[pos][2])
        
    def plate_vibrate(self, times):
        self.go_up()
        self.moveY(0)
        for i in range(times):
            self.send("G1 Y0 ; \n")
            self.send("G1 Y0.4 ; \n")
            sleep(0.1)
        sleep(1/self.xy_speed*times)
        
##if __name__ == '__main__':
     #dilution system test
##    printer = Printer("/dev/ttyUSB_DILPRINTER",1)
##    for i in printer.vialAcidDropoffPos:
##        if i[3] == 1:
##            i[2] = 33.6
##    printer.acidSetup()
##    printer.pippeteTipPickup()
##    printer.vialLiqiudPickup()
##    printer.dump()
##    for i in range(5):
##        printer.vialLiquidDispense(i)
##        printer.acidDispense(i)
##    printer.go_up()
##    printer.moveY(115)
##    printer.close()
    
##    printer = Printer("/dev/ttyUSB_RXNPRINTER",0)
##    for i in range(5):
##        printer.solidsDispense(i)
##        printer.stir(i)
##    printer.solidsPrime()
##    printer.close()
