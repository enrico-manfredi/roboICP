from printerLib import Printer
from arduinoLib import Arduino
from time import sleep

a = Arduino()
rxn = Printer("/dev/ttyUSB_RXNPRINTER",0)

shakes = 3
reset = True

##move plate to first position
rxn.solidsPrime()

if not reset:
    
    a.shake("hopper")
    a.hop_first() #open
    a.hop_next() #close
    
    ##pos 1 - ensure good side facing forwards
    rxn
    a.shake("hopper")
    a.hop_next() #open
    a.shake("hopper", shakes)
    a.hop_next() #close

    ##pos 2
    a.shake("hopper")
    a.hop_next() #open
    a.shake("hopper", shakes)
    a.hop_first() #close

##reset to good side
a.shake("hopper")
a.hop_first() #open
a.hop_next() #close
a.shake("hopper")
a.hop_next() # open
a.hop_next() #close
a.shake("hopper")
a.hop_next() #open
a.hop_first() #close
a.shake("hopper")

if not reset:
    rxn.solidsDispense(1)

    ##pos 3
    a.shake("hopper")
    a.hop_first() #open
    a.shake("hopper", shakes)
    a.hop_next() #close

    ##pos 4
    a.shake("hopper")
    a.hop_next() #open
    a.shake("hopper", shakes)
    a.hop_next() #close

    ##pos 5
    a.shake("hopper")
    a.hop_next() #open
    a.shake("hopper", shakes)
    a.hop_first() #close
