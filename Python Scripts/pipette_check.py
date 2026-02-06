from printerLib import Printer
from arduinoLib import Arduino

dil = Printer("/dev/ttyUSB_DILPRINTER",1)
a = Arduino()

for i in range(5):
    dil.pippeteTipPickup()
    dil.has_tip = False
    dil.go_up()
    a.tip_eject()
    a.vial_full_rot("fw")
    
##dil.pippeteTipPickup()
##dil.vialLiqiudPickup()
##
##for i in range(5):
##    dil.vialLiquidDispense(i)
##    
##dil.pippeteTipPickup()
##dil.moveZ(23.6)
##a.tip_eject()
##dil.has_tip = False
##
dil.close()
    