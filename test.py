import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
print(rm.list_resources()[0])
inst = rm.open_resource(rm.list_resources()[0])
print(inst.query("*IDN?"))