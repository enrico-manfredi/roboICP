from arduinoLib import Arduino
from printerLib import Printer

a = Arduino()
dil = Printer("/dev/ttyUSB_DILPRINTER",1)

a.lock("open")
a.act_reset()
a.rail_reset()

for i in range(5):
    print(i)
    if i == 0:
        a.nxt_syr(first = True)
    else:
        a.nxt_syr()
    dil.go_up()
    dil.moveY(114)
    input("check syringe alignment, press enter to proceed")
    a.act_ffw()
    a.lock("close")
    input("check head clearance, press enter to proceed")
    a.lock("open")
    a.act_reset()
    dil.moveY(0)
    
dil.close()