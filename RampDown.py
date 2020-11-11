import Keithley2410Control
import pyvisa

bias_supply=Keithley2410Control.keithley2410("ASRL5::INSTR")
bias_supply.set_current_protection(2.5E-6) # current protection in A
bias_supply.set_voltage_protection(1000) # voltage protection in V

bias_supply.ramp_down()
bias_supply.output_off()
