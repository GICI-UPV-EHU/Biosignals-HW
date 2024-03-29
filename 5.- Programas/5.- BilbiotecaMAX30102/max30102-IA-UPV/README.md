# max30102
MAX30102 Pulse Oximetry Sensor code for Raspberry Pi

## Info
The code originally comes from: https://github.com/vrano714/max30102-tutorial-raspberrypi
and secondlly from: https://github.com/doug-burrell/max30102

but with some modifications so that it doesn't require the interrupt pin and
instead polls by checking the read and write FIFO pointers. I've also added a
top level of code that encapsulates everything into a thread.

The original code is a Python port based on Maxim's reference design written to
run on an Arduino UNO: https://github.com/MaximIntegratedRefDesTeam/RD117_ARDUINO/


## Use as a library
To use the code, instantiate the `HeartRateMonitor` class found in `heartrate_monitor.py`.
The thread is used by running `start_sensor` and `stop_sensor`. While the thread
is running you can read `bpm` to get the active beats per minute. Note that a few
seconds are required to get a reliable BPM value and the sensor is very sensitive
to movement so a steady finger is required!

