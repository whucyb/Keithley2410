import pyvisa
import time
import warnings

class keithley2410:
    def __init__(self,resource_name):
        instlist=pyvisa.ResourceManager()
        #print(instlist.list_resources())
        self.kei2410=instlist.open_resource(resource_name)
        self.kei2410.timeout=25000
        self.cmpl='105E-6' # global current protection

    def testIO(self):
        message=self.kei2410.query('*IDN?')
        print(message)

    def set_current_protection(self,current):
        self.cmpl=str(current)
        self.kei2410.write(":sense:current:protection "+str(current))

    def set_voltage_protection(self,vol):
        self.kei2410.write(":source:voltage:range "+str(vol))

    def set_voltage(self,vol,speed=1):
        self.kei2410.write(":sense:current:protection "+self.cmpl)
        self.kei2410.write(":source:function voltage")
        self.kei2410.write(":source:voltage:mode fixed")
        print("******************************")
        print("From")
        vols=self.show_voltage()
        print("******************************")
        if -10<=vol<=10 and -10<=vols<=10:
            self.sweep(vols,vol,1,speed)
        elif -10<=vol<=10 and vols <-10:
            self.sweep(vols,-10,10,speed)
            self.sweep(-10,vol,1,speed)
        elif -10<=vol<=10 and vols>10:
            self.sweep(vols,10,10,speed)
            self.sweep(10,vol,1,speed)
        elif vol<-10 and -10<=vols<=10:
            self.sweep(vols,-10,1,speed)
            self.sweep(-10,vol,10,speed)
        elif vol>10 and -10<=vols<=10:
            self.sweep(vols,10,1,speed)
            self.sweep(10,vol,10,speed)
        else :
            self.sweep(vols,vol,10,speed)
        print("******************************")
        print("To")
        vols=self.show_voltage()
        print("******************************")
        self.beep()
        return vols

    def show_voltage(self):
        self.kei2410.write(":source:voltage:mode fixed")
        self.kei2410.write(":form:elem voltage")
        voltage=self.kei2410.query(":read?")
        # self.kei2410.timeout=5000
        print("voltage [V]: " + str(voltage))
        return float(str(voltage))

    def sweep(self, vols, vole, step, speed):
        if vols < vole: # vol start < vol end
            self.sweep_forward(vols,vole,step,speed)
        else:
            self.sweep_backward(vols,vole,step,speed)

    def sweep_forward(self, vols, vole, step,speed):
        # Conveter from V to mV
        mvols=vols*1000
        mvole=vole*1000+1
        mstep=step*1000
        for mvol in range(int(mvols),int(mvole),int(mstep)):
            vol=mvol/1000 # mV -> V
            self.kei2410.write(":source:voltage:level "+str(vol))
            time.sleep(5/speed)
            self.show_voltage()
            self.display_current()
            self.hit_compliance()

    def sweep_backward(self, vols, vole, step,speed):
        # Conveter from V to mV
        mvols=vols*1000
        mvole=vole*1000-1
        mstep=step*1000

        for mvol in range(int(mvols),int(mvole), -int(mstep)):
            vol=mvol/1000 # mV -> V
            self.kei2410.write(":source:voltage:level "+str(vol))
            time.sleep(5/speed)
            self.show_voltage()
            self.display_current()
            self.hit_compliance()

    def display_current(self):
        self.kei2410.write(":sense:function 'current'")
        # self.kei2410.write(":sense:current:range "+self.cmpl)
        self.kei2410.write(":sense:current:range:auto on")
        self.kei2410.write(":display:enable on")
        self.kei2410.write(":display:digits 7")
        self.kei2410.write(":form:elem current")
        current=self.kei2410.query(":read?")
        #self.kei2410.timeout=5000
        print("current [A]: " + str(current))
        return float(str(current))

    def hit_compliance(self):
        tripped=int(str(self.kei2410.query(":SENSE:CURRENT:PROTECTION:TRIPPED?")))
        if tripped:
            print("Hit the compliance "+self.cmpl+"A.")
        return tripped

    def ramp_down(self):
        print("Now ramping down...")                                                                                                                                                                  
        self.set_voltage(0,1)
        self.beep()


    def output_on(self):
        self.kei2410.write(":output on")
        print("Output on")

    def output_off(self):
        self.kei2410.write(":output off")
        print("Output off")

    def beep(self, freq=1046.50, duration=0.3):
        self.kei2410.write(":system:beeper "+str(freq)+", "+str(duration))
        time.sleep(duration)

    def filter_on(self, count=20, mode="repeat"):
        self.kei2410.write(":sense:average:count "+str(count))
        self.kei2410.write(":sense:average:tcontrol "+mode) # repeat or moving
        self.kei2410.write(":sense:average:state on")

    def filter_off(self):
        self.kei2410.write(":sense:average:state off")

    def __del__(self):
        self.kei2410.close()

if __name__=="__main__":
    kei2410=keithley2410("ASRL6::INSTR")
    kei2410.testIO()
