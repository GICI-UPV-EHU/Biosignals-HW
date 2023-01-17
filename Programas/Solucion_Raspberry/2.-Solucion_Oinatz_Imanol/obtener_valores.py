
import sys
import multiprocessing as mpr

### importamos las librerías de sensores
import max30102
import Grove_adc
###


m = max30102.MAX30102()


class GSR_ECG_sensor:
        def __init__(self, channel):
                self.channel = channel
                self.adc = Grove_adc.ADC()
        
        def GSR_ECG(self):
                value = self.adc.read(self.channel)
                return value


# Se utilizan 100 muestras para calcular HR/SpO2 en cada loop
    
def coger_datos_pox():

    red, ir = m.read_fifo()
    return (red, ir)

def coger_datos_gsr():

    gsr = GSR_ECG_sensor(0)
    Ratio_val = gsr.GSR_ECG()
    V_val = 3.3 * Ratio_val/999
    V_divisor = V_val/21
    if V_divisor == 0:
        Val_siem = 0
    else: 
        R_gsr = 47000*(5/V_divisor-1)
        Val_siem = 1/R_gsr*1000000
    return(Val_siem)

def coger_datos_ecg():

    ecg = GSR_ECG_sensor(2)
    ECG_val = ecg.GSR_ECG()
    return(ECG_val)


