from __future__ import print_function
from ctypes import addressof
from ssl import CHANNEL_BINDING_TYPES
from time import sleep

import RPi.GPIO as GPIO
import smbus

# Direcciónes de los registros

INT_STATUS   = 0x00  # Which interrupts are tripped

INT_ENABLE   = 0x01  # Which interrupts are active

FIFO_WR_PTR  = 0x02  # Where data is being written
OVRFLOW_CTR  = 0x03  # Number of lost samples
FIFO_RD_PTR  = 0x04  # Where to read from
FIFO_DATA    = 0x05  # Ouput data buffer
FIFO_CONFIG  = 0x08  # FIFO configuration

MODE_CONFIG  = 0x06  # Control register
SPO2_CONFIG  = 0x07  # Oximetry settings
LED_CONFIG   = 0x09  # Pulse width and power of LEDs

TEMP_INTG    = 0x16  # Temperature value, whole number
TEMP_FRAC    = 0x17  # Temperature value, fraction

REV_ID       = 0xFE  # Part revision
PART_ID      = 0xFF  # Part ID, normally 0x11

class MAX30100():
    
    def __init__(self, channel=1, address=0x57, gpio_pin=7):
        print("Channel: {0}, address: 0x{1:x}".format(channel, address))
        self.address = address
        self.channel = channel
        self.bus = smbus.SMBus(self.channel)
        self.interrupt = gpio_pin

        # Establecer modo GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.interrupt, GPIO.IN)

        self.reset()

        sleep(1)  # wait 1 sec

        # read & clear interrupt register (read 1 byte)
        reg_data = self.bus.read_i2c_block_data(self.address, INT_STATUS, 1)
        # print("[SETUP] reset complete with interrupt register0: {0}".format(reg_data))
        self.setup()
        # print("[SETUP] setup complete")
        
    def shutdown(self):
        
        self.bus.write_i2c_block_data(self.address, MODE_CONFIG, [0x80])
        
    def reset(self):
        
        self.bus.write_i2c_block_data(self.address, MODE_CONFIG, [0x40])
        
    def setup(self, led_mode=0x03):
        """
        This will setup the device with the values written in sample Arduino code.
        """
        # INTR setting
        # 0xc0 : A_FULL_EN and PPG_RDY_EN = Interrupt will be triggered when
        # fifo almost full & new fifo data ready
        self.bus.write_i2c_block_data(self.address, INT_ENABLE, [0xc0])

        # FIFO_WR_PTR[4:0]
        self.bus.write_i2c_block_data(self.address, FIFO_WR_PTR, [0x00])
        # OVF_COUNTER[4:0]
        self.bus.write_i2c_block_data(self.address, OVRFLOW_CTR, [0x00])
        # FIFO_RD_PTR[4:0]
        self.bus.write_i2c_block_data(self.address, FIFO_RD_PTR, [0x00])

        # 0b 0100 1111
        # sample avg = 4, fifo rollover = false, fifo almost full = 17
        self.bus.write_i2c_block_data(self.address, FIFO_CONFIG, [0x4f])

        # 0x02 for read-only, 0x03 for SpO2 mode, 0x07 multimode LED
        self.bus.write_i2c_block_data(self.address, MODE_CONFIG, [led_mode])
        # 0b 0010 0111
        # SPO2_ADC range = 4096nA, SPO2 sample rate = 100Hz, LED pulse-width = 411uS
        self.bus.write_i2c_block_data(self.address, SPO2_CONFIG, [0x27])

        # choose value for ~7mA for LED1
        self.bus.write_i2c_block_data(self.address, LED_CONFIG, [0x24])

    def set_config(self, reg, value):
        self.bus.write_i2c_block_data(self.address, reg, value)

    def read_fifo(self):
        """
        This function will read the data register.
        """
        red_led = None
        ir_led = None

        # read 1 byte from registers (values are discarded)
        reg_INTR1 = self.bus.read_i2c_block_data(self.address, INT_STATUS, 1)

        # read 6-byte data from the device
        d = self.bus.read_i2c_block_data(self.address, FIFO_DATA, 6)

        # mask MSB [23:18]
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF
        
        return red_led, ir_led

    def read_sequential(self, amount=100):
        """
        This function will read the red-led and ir-led `amount` times.
        This works as blocking function.
        """
        red_buf = []
        ir_buf = []
        for i in range(amount):
            while(GPIO.input(self.interrupt) == 1):
                # wait for interrupt signal, which means the data is available
                # do nothing here
                pass

            red, ir = self.read_fifo()

            red_buf.append(red)
            ir_buf.append(ir)

        return red_buf, ir_buf
    
    