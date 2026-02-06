from arduinoLib import Arduino
from time import sleep

a = Arduino()

a.lock("open")
a.act_reset()
a.rail_reset()

for i in range(5):
    if i == 0:
        a.nxt_syr(first = True)
    else:
        a.nxt_syr()
    a.act_ffw()
    a.lock("close")
    for j in range(2):
        a.act_reset()
        a.act_ffw()
    a.lock("open")
    a.act_reset()