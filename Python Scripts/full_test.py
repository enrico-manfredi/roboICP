from printerLib import Printer
from arduinoLib import Arduino
from time import sleep, time
from picamera import PiCamera

##control objects init
##camera = PiCamera()
a = Arduino()
dil = Printer("/dev/ttyUSB_DILPRINTER",1)
rxn = Printer("/dev/ttyUSB_RXNPRINTER",0)

##picam params
##camera.resolution = (1280, 720)
##camera.hflip = True
##file_name = "/home/pi/Pictures/video_" + str(time()) + ".h264"
##camera.start_recording(file_name)

##home the actuators in the syringe system
a.lock("open")
a.act_reset()
a.rail_reset()

##acid priming
dil.acidSetup()
a.acid_pump(150, "fw")
a.acid_pump(2, "bw")
dil.go_up()

##set initial dispensation point
d_pos = 0

##prime powder before first run
rxn.solidsDispense(0)
a.hop_first()
for i in range(3):
    a.shake("hopper")
    a.shake("plate")
a.hop_next()

##timing
start_time = 0
finish_time = 0
dil_times = []

for i in range(5):
    print(i)
    ##solid dispensing logic
    if i == 2:
        ##set rank for next runs
        d_pos = 1
        ##prime powder for next rank
        rxn.solidsDispense(0)
        a.hop_first()
        for i in range(3):
            a.shake("hopper")
            a.shake("plate")
        a.hop_neg_next()
    ##dispense
    rxn.solidsDispense(d_pos)
    a.hop_next()
    for j in range(5):
        a.shake("hopper")
        a.shake("plate")
    ##close dispensing hole
    if i == 1 or i == 4:
        a.hop_first()
    else:
        a.hop_next()
    start_time = time()
    rxn.stir(i)
    a.stir(10)
    rxn.go_up()
    ##move to next syringe
    if i == 0:
        a.nxt_syr(first = True)
    else:
        a.nxt_syr()
    ##move dil system plate forward to accept filtrate
    if i < 0: ##set to 0 for all, set n to exclude up to position n
        continue
    dil.moveY(114)
    ##cycle syringes with linear actuator
    a.lock("open")
    a.act_ffw()
    a.lock("close")
    a.act_reset()
    sleep(30)
    a.mov_act(130, "fw")
    sleep(300)
    a.lock("open")
    ##move linear actuator clear of syringe heads
    a.act_reset()
    ##pick up and dispense filtrate into waiting vial
    dil.pippeteTipPickup()
    dil.vialLiqiudPickup()
    a.liq_press()
    dil.vialLiquidDispense(i)
    a.liq_press()
    ##eject the tip into front waste area
    dil.dump()
    a.tip_eject()
    ##move the carousel out of the way if it inteferes with acid dispensation
    if dil.vialAcidDropoffPos[i][3] == 1:
        a.car_hold("on")
        a.vial_half_rot("fw")
        dil.acidDispense(i)
        a.acid_pump(40, "fw")
        a.acid_pump(2, "bw")
        dil.go_up()
        a.vial_half_rot("bw")
    else:
        dil.acidDispense(i)
        a.acid_pump(40, "fw")
        a.acid_pump(2, "bw")
        dil.go_up()
    finish_time = time()
    dil_times.append(finish_time - start_time)
    ##move carousel to next sample
    a.vial_full_rot("fw")

##camera.stop_recording()
dil.close()
rxn.close()

print("\n")
print(dil_times)