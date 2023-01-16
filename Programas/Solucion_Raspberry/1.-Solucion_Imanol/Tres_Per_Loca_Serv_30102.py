#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 12 / 05 / 2022                      ##
##                                                             ## 
#################################################################

# ---------------------------------- Enunciado ---------------------------------- #

'''
Una vez ya se han creadop las tres tareas periódicas, y funcionan correctamente. 
Se quiere desarrollar una subida de datos a una base de datros de POSTGRES.

En este primer intento se ejecutará todo de forma local, es decir, todos los 
movimientos de datos se harán dentro de la propia raspberry sin acceso a internet
y sin involucrar a otos dispositivos.

Sensor de POX --> MAX 30102
Sensor de GSR --> ????? (no implementado)

'''

# ---------------------------------- Programa ---------------------------------- #

import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
import max30102 # Biblioteca con la cual se utiliza en sensor MAX30100
from datetime import datetime
import time
import BiblioTareasPeriodicas_ServerLocal
import csv

import psycopg2
import Grove_adc
import os
# ------------ Funciones que irán dentro de las tareas ------------ #

def CogerGuardarDatosPOX(a_ir, a_r, a_t):
        a_t.append(datetime.now())#.strftime('%H:%M:%S.%f'))
        rojo = 0
        infrarrojo = 0

        rojo, infrarrojo= mx30.read_fifo()  # se recoge el valor infra y rojo

    # ------------- Guardar datos en los arrays -------------#
    
        a_ir.append(infrarrojo)
        a_r.append(rojo)
        #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))


def CogerGuardarDatosGSR(a_gsr, a_t):
        gsr = GSR_ECG_sensor(0)
        Ratio_val = gsr.GSR_ECG()
        V_val = 3.3 * Ratio_val/999
        V_divisor = V_val/21
        if V_divisor == 0:
            Val_siem = 0
        else: 
            R_gsr = 47000*(5/V_divisor-1)
            Val_siem = 1/R_gsr*1000000

        a_gsr.append(Val_siem)
        #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))
        a_t.append(datetime.now())#.strftime('%H%M%S%f'))
        
def CogerGuardarDatosECG(a_ecg, a_t):
        ecg = GSR_ECG_sensor(2)
        ECG_val = ecg.GSR_ECG()


        a_ecg.append(ECG_val)
        #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))
        a_t.append(datetime.now())#.strftime('%H%M%S%f'))
        
def coms(a_ir,a_rojo, a_t_P, a_gsr, a_t_G, a_ecg, a_t_E):
        print ("Infrarrojo: " , len(a_ir), "Rojo: ", len(a_gsr))
        
        with open('/home/pi/Desktop/Data/POX.csv', 'w', newline='') as POX_CSV:
                w = csv.writer(POX_CSV)
                for i in range(len(a_ir)-1):
                        w.writerow([a_t_P[i], a_rojo[i], a_ir[i]])
                        
        with open('/home/pi/Desktop/Data/GSR.csv', "w", newline = '') as GSR_CSV:
                w = csv.writer(GSR_CSV)
                for i in range(len(a_gsr)-1):
                        w.writerow([a_t_G[i
                        ], a_gsr[i]])
        
        with open('/home/pi/Desktop/Data/ECG.csv', "w", newline = '') as ECG_CSV:
                w = csv.writer(ECG_CSV)
                for i in range(len(a_ecg)-1):
                        w.writerow([a_t_E[i
                        ], a_ecg[i]])
        


        conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')
        cur = conn.cursor()
        pox = open('/home/pi/Desktop/Data/POX.csv', 'r')
        gsr = open('/home/pi/Desktop/Data/GSR.csv', 'r')
        ecg = open('/home/pi/Desktop/Data/ECG.csv', 'r')

        cur.copy_from(pox, 'pox', sep=",")
        pox.close()
        cur.copy_from(gsr, 'gsr', sep=",")
        gsr.close()
        cur.copy_from(ecg, 'ecg', sep=",")
        ecg.close()

        cur.close()
        conn.commit()
        conn.close()
                                                
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        a_t_P[:] = []
        a_t_G[:] = []
        os.remove('/home/pi/Desktop/Data/POX.csv')
        os.remove('/home/pi/Desktop/Data/GSR.csv')
        os.remove('/home/pi/Desktop/Data/ECG.csv')
        print("Limpios: ")
        print(" \n")
        print(" \n")

        

# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    mx30 = max30102.MAX30102()

    class GSR_ECG_sensor:
        def __init__(self, channel):
                self.channel = channel
                self.adc = Grove_adc.ADC()
        
        def GSR_ECG(self):
                value = self.adc.read(self.channel)
                return value
    
    # Se crean objetos protegidos mediante manager
    mng = mp.Manager()
    y_Ir = mng.list()
    y_Rojo = mng.list()
    y_t_POX = mng.list()
    
    y_GSR = mng.list()
    y_t_GSR = mng.list()
    
    y_ECG = mng.list()
    y_t_ECG = mng.list()
    
    #
    a=1
    #
    
    
    tiempo0 = time.time() # Tiempo inicial
    
    tarea1 = mp.Process(target = BiblioTareasPeriodicas_ServerLocal.Tarea_Periodica_Sensores_3Arr, args = (tiempo0, 1, 0.1, 0.1, CogerGuardarDatosPOX, y_Ir,y_Rojo, y_t_POX))
    tarea2 = mp.Process(target = BiblioTareasPeriodicas_ServerLocal.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 2, 0.1, 0.1, CogerGuardarDatosGSR, y_GSR, y_t_GSR))
    tarea3 = mp.Process(target = BiblioTareasPeriodicas_ServerLocal.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 3, 0.01, 0.01, CogerGuardarDatosECG, y_ECG, y_t_ECG))
    tarea4 = mp.Process(target = BiblioTareasPeriodicas_ServerLocal.Tarea_Periodica_Sensores_7Arr_Duerme_Ini, args = (tiempo0, 4, 10, 61, coms, y_Ir, y_Rojo, y_t_POX, y_GSR, y_t_GSR, y_ECG, y_t_ECG))

    
    tarea1.start()
    tarea2.start()
    tarea3.start()
    tarea4.start()
    
    tarea1.join()
    tarea2.join()
    tarea3.join()
    tarea4.join()
    
    
    ###################################################
    #                      CONCLUSION                 #
    
# Se ha solucionado haciendo que en la tarea de CSV se
# guarde en variables internas de la tarea los arrays 
# de datos. De esta manera, no hace falta parar las 
# tareas de adquisición de datos, si no que pueden seguir
# todas en paralelo, ya que no trabajan con los mimos
# arrays

