import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)

while 1:
    ser.write(70000)
    time.sleep(10)