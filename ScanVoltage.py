import Keithley2410Control
import pyvisa
import time
import numpy as np

bias_supply=Keithley2410Control.keithley2410("ASRL6::INSTR")
bias_supply.set_current_protection(2.5E-6) # current protection in A
bias_supply.set_voltage_protection(500) # voltage protection in V
HVrange=-10
if HVrange > 0:
    sign = 1
else:
    sign = -1
bias_supply.filter_off()
time_start=time.time()

vols=[]
mvols=[]
current=[]
iStart=0
iEnd=HVrange
iStep=sign
for iBias in range(iStart,iEnd,iStep):
    bias_supply.output_on()
    biasvol=iBias
    vols.append(biasvol)
    mvols.append(bias_supply.set_voltage(biasvol))
    time.sleep(0.5)
    current.append(bias_supply.display_current())
    if bias_supply.hit_compliance():
        break

print("Bias Vols: "+str(vols))
print("Measured vols: "+str(mvols))
print("Current: "+str(current))

data=[vols,mvols,current]
dataarray=np.array(data)

time_top=time.time()
print("Ramping up takes %3.0f s." % (time_top-time_start))

print("Now ramping down...")
bias_supply.set_voltage(0*1e3,5)
bias_supply.output_off()
bias_supply.beep()
time_end=time.time()

print("Ramping up time:\t%3.0f s" % (time_top-time_start))
print("Ramping down time:\t%3.0f s" % (time_end-time_top))
print("Total time:\t\t%3.0f m %2.0f s" % ((time_end-time_start)//60, (time_end-time_start)%60))
