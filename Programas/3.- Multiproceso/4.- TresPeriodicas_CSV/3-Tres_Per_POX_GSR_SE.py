#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 12 / 05 / 2022                      ##
##                                                             ## 
#################################################################

# ---------------------------------- Enunciado ---------------------------------- #

''' 
Una vez hecho el cambio de sensor POX, se comienza a escribir el codigo para la inclusión 
de un sensor analógico GSR (Galvanic Skin Response). Para añadir este sensor es necesario 
un ADC, conversor analógico - digital, ya que las raspberry no tienen ningun ADC

En este primera versión del código tiene como objetivo principal la inclusión del ADC
propio de la compañia Seeed-Studio , misma compañia creadora del sensor.
La elección en primera instancia de este ADC, es que esta compañia tiene desarrollada una 
biblioteca para la correcta ejecución del conversor -- > https://github.com/Seeed-Studio/grove.py

Por lo que para el primer acercamiento a los sensores analógicos, será más sencillo siguiendo
los pasos de su página web
https://wiki.seeedstudio.com/Grove-GSR_Sensor/

'''

# ---------------------------------- Programa ---------------------------------- #

import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
import max30102 # Biblioteca con la cual se utiliza en sensor MAX30100
from datetime import datetime
import time
import BiblioTareasPeriodicas
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


# ------------ Funciones que irán dentro de las tareas ------------ #

def CogerGuardarDatosPOX(a_ir, a_r, a_t):
        a_t.append(datetime.now()) #.strftime('%M:%S.%f'))
        rojo = 0
        infrarrojo = 0
        
        rojo, infrarrojo= mx30.read_fifo()  # se recoge el valor del led infrarrojo

    # ------------- Guardar datos en los arrays -------------#
    
        a_ir.append(infrarrojo)
        a_r.append(rojo)
        #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))


def CogerGuardarDatosGSR(a_gsr, a_t):
        # global a
        # a_pox.append(a)
        # #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))
        # a = a + 1
        a_t.append(datetime.now()) #.strftime('%M:%S.%f'))
        GSR_val = 0
        GSR_val = gsr.GSR()
        a_gsr.append(GSR_val)

        
        
def coms(a_ir,a_rojo, a_t_P, a_gsr, a_t_G):
        print ("Infrarrojo: " , len(a_ir), "Rojo: ", len(a_gsr))
        
        with open('/home/pi/Desktop/Data/POX.csv', 'a+', newline='') as POX_CSV:
                w = csv.writer(POX_CSV)
                for i in range(len(a_ir)-1):
                        w.writerow([a_t_P[i], a_rojo[i], a_ir[i]])
                        
        with open('/home/pi/Desktop/Data/GSR.csv', "a+", newline = '') as GSR_CSV:
                w = csv.writer(GSR_CSV)
                for i in range(len(a_gsr)-1):
                        w.writerow([a_t_G[i], a_gsr[i]])
                                                
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        a_t_P[:] = []
        a_t_G[:] = []
        print("Limpios: ")
        print(" \n")
        print(" \n")

        

# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    mx30 = max30102.MAX30102()

    gsr = GSR_sensor(0)  # se introduce un 0 ya que el sensore está
                         # conectado al grupo de pines A0
    
    # Se crean objetos protegidos mediante manager
    mng = mp.Manager()
    y_Ir = mng.list()
    y_Rojo = mng.list()
    y_t_POX = mng.list()
    
    y_GSR = mng.list()
    y_t_GSR = mng.list()
    
    
    
    #
    a=1
    #
    
    Flag_POX = mp.Event()
    Flag_GSR = mp.Event()
    Flag_GSR.clear()
    Flag_POX.set()
    
    tiempo0 = time.time() # Tiempo inicial
    
    tarea1 = mp.Process(target = BiblioTareasPeriodicas.Tarea_Periodica_Sensores_3Arr, args = (tiempo0, 1, 0.02, 0.015, CogerGuardarDatosPOX, y_Ir,y_Rojo, y_t_POX))
    tarea2 = mp.Process(target = BiblioTareasPeriodicas.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 2, 0.05, 0.04, CogerGuardarDatosGSR, y_GSR, y_t_GSR))
    tarea3 = mp.Process(target = BiblioTareasPeriodicas.Tarea_Periodica_Sensores_5Arr_Duerme_Ini, args = (tiempo0, 3, 10, 10, coms, y_Ir, y_Rojo, y_t_POX, y_GSR, y_t_GSR))
    
    tarea1.start()
    tarea2.start()
    tarea3.start()
    
    tarea1.join()
    tarea2.join()
    tarea3.join()
    
    
    ###################################################
    #                      CONCLUSION                 #
    
# Se ha solucionado haciendo que en la tarea de CSV se
# guarde en variables internas de la tarea los arrays 
# de datos. De esta manera, no hace falta parar las 
# tareas de adquisición de datos, si no que pueden seguir
# todas en paralelo, ya que no trabajan con los mimos
# arrays

###################### Siguiente Prueba ##################
# ¿Se puede hacer una comunicación a algún sitio de esta manera? 