
from doctest import ELLIPSIS_MARKER
from smbus import SMBus

addr = 0x8
bus = SMBus(1)
numb = 1

print( ' Mete un 1 para ENCENDER y un 0 para Apagar')
while numb == 1:

    ledstate = input(">>>>>>   ")

    if ledstate == '1':
        bus.write_(addr, 0x1)
    elif ledstate == '0':
        bus.write_byte(addr, 0x0)
    else:
        numb = 0