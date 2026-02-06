from printerLib import Printer
from arduinoLib import Arduino

a = Arduino()
dil = Printer("/dev/ttyUSB_DILPRINTER",1)

dil.acidSetup()
a.acid_pump(150, "fw")
a.acid_pump(2, "bw")
dil.go_up()

acid = True

for i in range(5):
    if dil.vialAcidDropoffPos[i][3] == 1:
        a.car_hodl("on")
        a.vial_half_rot("fw")
        dil.acidDispense(i)
        input("check alignment for pos "+str(i))
        if acid:
            a.acid_pump(10, "fw")
            a.acid_pump(2, "bw")
        dil.go_up()
        a.vial_half_rot("bw")
    else:
        dil.acidDispense(i)
        input("check alignment for pos "+str(i))
        if acid:
            a.acid_pump(10, "fw")
            a.acid_pump(2, "bw")
        dil.go_up()
        
dil.close()
