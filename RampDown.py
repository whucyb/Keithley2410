import Keithley2410Control
import pyvisa

bias_supply=Keithley2410Control.keithley2410("ASRL6::INSTR")
bias_supply.set_current_protection(2.5E-6) # current protection in A
bias_supply.set_voltage_protection(500) # voltage protection in V

print("Now ramping down...")
bias_supply.set_voltage(0*1e3,5)
bias_supply.output_off()
bias_supply.beep()
