import max30100_Imanol
import hrcalc

m = max30100_Imanol.MAX30100()

# 100 samples are read and used for HR/SpO2 calculation in a single loop
while True:
    red, ir = m.read_sequential()
    print(hrcalc.calc_hr_and_spo2(ir, red))

