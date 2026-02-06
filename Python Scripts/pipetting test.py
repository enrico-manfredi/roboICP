from printerLib import Printer
from arduinoLib import Arduino
from time import sleep

a = Arduino()
dil = Printer("/dev/ttyUSB_DILPRINTER",1)

for i in range(5):
    ##pick up and dispense filtrate into waiting vial
    dil.pippeteTipPickup()
    dil.vialLiqiudPickup()
    a.liq_press("press")
    sleep(2)
    a.liq_press("release")
    dil.vialLiquidDispense(i)
    a.liq_press("press", hard = True)
    dil.moveZ(10)
    dil.go_up()
    a.liq_press("release")
    ##eject the tip into front waste area
    dil.dump()
    a.tip_eject()
    input("replace pipette and press enter to continue")