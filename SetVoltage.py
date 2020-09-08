import Keithley2410Control
import pyvisa
import sys

bias_supply=Keithley2410Control.keithley2410("ASRL6::INSTR")
bias_supply.set_current_protection(2.5E-6) # current protection in A
bias_supply.set_voltage_protection(500) # voltage protection in V
HV=int(sys.argv[1])

bias_supply.filter_off()
bias_supply.output_on()
bias_supply.set_voltage(HV,5)
bias_supply.display_current()
