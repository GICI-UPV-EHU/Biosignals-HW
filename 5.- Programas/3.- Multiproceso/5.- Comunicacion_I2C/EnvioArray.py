import smbus
import time

bus = smbus.SMBus(1)
addres = 0x8
a = 0

a_r = []
for i in range(5000):
    a_r.append(a)
    a = a + 1
    if a == 256:
        a = 0
bus.write_i2c_block_data( addres, a_r[0], a_r[1:len(a_r)])

