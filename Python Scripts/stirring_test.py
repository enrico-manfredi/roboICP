from printerLib import Printer
from arduinoLib import Arduino

a = Arduino()
rxn = Printer("/dev/ttyUSB_RXNPRINTER",0)

for i in range(5):
    rxn.stir(i)
    a.stir(10)
    rxn.go_up()
    
rxn.close()