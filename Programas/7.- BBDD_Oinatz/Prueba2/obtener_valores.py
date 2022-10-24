
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
        
        def GSR(self):
                value = self.adc.read(self.channel)
                return value


# Se utilizan 100 muestras para calcular HR/SpO2 en cada loop
    
def coger_datos_pox():

    red, ir = m.read_fifo()
    return (red, ir)

def coger_datos_gsr():

    gsr = GSR_ECG_sensor(0)
    GSR_val = gsr.GSR()
    return(GSR_val)

def coger_datos_ecg():

    ecg = GSR_ECG_sensor(2)
    ECG_val = ecg.GSR()
    v_real  = ECG_val * (3.3/999)/39.3142
    try :
        v_resis = (5.0/v_real+1)*4700
        v_siem  = (1/v_resis)*1000000
    except(Exception):
        v_resis = 0
    return(v_resis)


