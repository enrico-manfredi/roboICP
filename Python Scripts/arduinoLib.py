from serial import Serial
from time import sleep


class Arduino:
    def __init__(self):
        self.port = "/dev/ttyACM0"
        self.open()

    def open(self):
        self.ser = Serial(self.port)
        sleep(1)
        
    def send(self, command):
        self.ser.write(str.encode(str(command)+"\n"))
        print("sent "+str(command))
        #print(self.ser.readline().decode("utf-8"))

    def vial_half_rot(self, dir):
        print("carousel half rotation "+dir)
        if dir == "fw":
            self.send(2)
        elif dir == "bw":
            self.send(3)
        else:
            raise
        sleep(1.5)
        
    def vial_full_rot(self, dir):
        if dir == "fw":
            self.send(2)
            sleep(1.5)
            self.send(2)
        elif dir == "bw":
            self.send(3)
            sleep(1.5)
            self.send(3)
        else:
            raise
        sleep(1.5)
    
    def nxt_syr(self, first = False):
        if first:
            self.send(4)
            sleep(5)
        elif not first:
            self.send(5)
            sleep(9)
        else:
            raise
        
    def rail_reset(self):
        self.send(6)
        sleep(42)
        
    def mov_act(self, steps, dir, delay = 0.2):
        cmd = 0
        if dir == "bw":
            cmd = 8
        elif dir == "fw":
            cmd = 7
        else:
            raise
        for i in range(steps):
            self.send(cmd)
            sleep(delay)
            
    def acid_pump(self, steps, dir):
        cmd = 0
        if dir == "fw":
            cmd = 10
        elif dir == "bw":
            cmd = 9
        else:
            raise
        for i in range(steps):
            self.send(cmd)
            sleep(0.2)
        
    def lock(self, dir):
        if dir == "open":
            self.send(12)
        elif dir == "close":
            self.send(11)
        sleep(1)
        
    def tip_eject(self):
        self.send(14)
        sleep(2.5)
        
    def liq_press(self, dir, hard = False):
        if dir == "press":
            if hard:
                self.send(27)
            else:
                self.send(15)
            sleep(3)
        if dir == "release":
            self.send(28)
            sleep(2)
        
    def hop_first(self):
        self.send(16)
        sleep(2)
        
    def hop_next(self):
        self.send(17)
        sleep(2)
        
    def shake(self, obj, times = 1):
        cmd = 0
        if obj == "hopper":
            cmd = 18
        elif obj == "plate":
            cmd = 19
        else:
            raise
        for i in range(times):
            self.send(cmd)
            sleep(1.5)
    
    def stir(self, time):
        for t in range(time):
            self.send(20)
            sleep(1.2)
            
    def act_reset(self):
        self.send(21)
        sleep(12)
        
    def act_ffw(self):
        self.send(22)
        sleep(12)
        
    def stir_now(self):
        self.send(23)
        
    def hop_neg_next(self):
        self.send(24)
        sleep(2)
        
    def car_hold(self, mode):
        if mode == "on":
            self.send(25)
        elif mode == "off":
            self.send(26)
        else:
            raise
        sleep(0.5)
        
##if __name__ == "__main__":
##    a = Arduino()
##    a.vial_half_rot("fw")
##    print(1)
##    a.vial_half_rot("bw")
##    print(2)
##    a.vial_full_rot("fw")
##    print(3)
##    a.vial_full_rot("bw")
##    print(4)
##    a.nxt_syr(first = True)
##    print(5)
##    for i in range(4):
##        a.nxt_syr()
##        print(6+i)
##    a.rail_reset()
##    print(10)
##    a.mov_act(10,"fw")
##    print(11)
##    a.mov_act(10, "bw")
##    print(12)
##    a.acid_pump(10, "fw")
##    print(13)
##    a.acid_pump(10, "bw")
##    print(14)
##    a.lock("close")
##    print(15)
##    a.lock("open")
##    print(16)
##    a.tip_eject()
##    print(17)
##    a.liq_press()
##    print(18)
##    print(24)
##    a.shake("hopper", 10)
##    print(25)
##    a.shake("plate", 10)
##    print(26)
##    a.stir(20)
##    print(27)
##    a.act_ffw()
##    print(28)
##    a.act_reset()
##    print(29)    