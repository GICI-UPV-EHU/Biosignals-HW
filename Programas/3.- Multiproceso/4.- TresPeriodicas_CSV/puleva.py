import math
import sys
import time
import Grove_adc

class GroveGSRSensor:
     
    def __init__(self, channel):
        self.channel = channel
        self.adc = Grove_adc.ADC()
 
    @property
    def GSR(self):
        value = self.adc.read_voltage(self.channel)
        return value
 
 
 
def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)
 
    sensor = GroveGSRSensor(int(sys.argv[1]))
 
    print('Detecting...')
    while True:
        print('GSR value: {0}'.format(sensor.GSR))
        time.sleep(.3)
 
if __name__ == '__main__':
    main()