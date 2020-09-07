import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
if len(rm.list_resources()) != 0:
    print(rm.list_resources()[0])
    inst = rm.open_resource(rm.list_resources()[0])
    print(inst.query("*IDN?"))
