from servoLib import *
from actuatorLib import *
from linearRailLib import *
from pumpLib import *
from rotationVialLib import *
from printerLib import *
import time


if __name__ == "__main__":
    
    GPIO.setmode(GPIO.BOARD)
    
    
    actuator = actuator()
    pump = acidPump()
    linearRail = linearRail()
    rotationVial = rotationVial()
    lock = servoLock(31)
    printer = printer()
    pippeteTip = servoTip(15)
    pippeteLiquid = servoLiquid(7)
    
    printer.dump()
    pump.calibrate()
    
    
    
    for liquid_number in range(5):
        linearRail.moveToSyringe(liquid_number)
        printer.moveY(0)
        rotationVial.moveToVialFilling()
        actuator.getSyringe()
        lock.lock()
        actuator.pullSyringe()
        actuator.pushSyringe()
        lock.open()
        actuator.reset()
        rotationVial.moveToVial()
        
        print("picking ouo tip")
        printer.pippeteTipPickup()
        time.sleep(30)
        print("liquid pick up")
        printer.vialLiqiudPickup()
        time.sleep(30)
        
        pippeteLiquid.press()
        time.sleep(2)
        pippeteLiquid.release()
        
        print("dispensing pick up")
        printer.vialLiquidDispense(liquid_number)
        time.sleep(30)
        
        pippeteLiquid.press()
        
        print("acid dispence pick up")
        printer.acidDispence(liquid_number)
        time.sleep(20)
        
        pippeteLiquid.release()
        
        pump.dispense(3)
        
        printer.dump()
        time.sleep(5)
        
        pippeteTip.press()
        time.sleep(1)
        pippeteTip.release()
        
        rotationVial.nextVial()
    
    GPIO.cleanup()
    