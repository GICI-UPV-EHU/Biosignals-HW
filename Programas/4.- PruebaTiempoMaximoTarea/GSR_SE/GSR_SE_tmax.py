#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 26 / 04 / 2022                      ##
##                                                             ## 
#################################################################

# ---------------------------------- Enunciado ---------------------------------- #

# Probar a ver si se logra resolver que las tres tareas periodicas se sincronicen
# correctamente, ya que el tiempo que tarda la tercera de llas peta las demás en 
# los siguientes ciclos


# ---------------------------------- Programa ---------------------------------- #

import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
from datetime import datetime
import time
import Tareas2
import csv

# Bibliotecas para el ADC de Seeed-studio

import Grove_adc

'''
Se crea una clase con las funciuones de inicialización y adquisición de datos del sensor GSR
'''
class GSR_sensor:
        def __init__(self, channel):
                self.channel = channel
                self.adc = Grove_adc.ADC()
        
        def GSR(self):
                value = self.adc.read(self.channel)
                return value

# ------------ Funciones que irán dentro de las tareas ------------ 


def CogerGuardarDatosGSR(a_gsr, a_t):
        a_t.append(datetime.now()) #.strftime('%M:%S.%f'))
        GSR_val = 0
        GSR_val = gsr.GSR()
        a_gsr.append(GSR_val)
        
def coms(a_ir,a_rojo, a_t_P, a_gsr, a_t_G):

        with open('/home/pi/Desktop/Data/GSR.csv', "a+", newline = '') as GSR_CSV:
                w = csv.writer(GSR_CSV)
                for i in range(len(a_gsr)-1):
                        w.writerow([a_t_G[i], a_gsr[i]])
                                                
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        

# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    gsr = GSR_sensor(0)  # se introduce un 0 ya que el sensore está
                         # conectado al grupo de pines A0

    # Se crean objetos protegidos mediante manager
    mng = mp.Manager()
    
    y_GSR = mng.list()
    y_t_GSR = mng.list()

    Flag_GSR = mp.Event()
    Flag_GSR.clear()
    
    tiempo0 = time.time() # Tiempo inicial
    
    tarea2 = mp.Process(target = Tareas2.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 2, 0.05, 0.04, CogerGuardarDatosGSR, y_GSR, y_t_GSR))
   
    tarea2.start()

    tarea2.join()
    