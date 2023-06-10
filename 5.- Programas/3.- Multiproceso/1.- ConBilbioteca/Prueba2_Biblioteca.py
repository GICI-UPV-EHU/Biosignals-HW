#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 13 / 04 / 2022                      ##
##                                                             ## 
#################################################################

# ---------------------------------- Enunciado ---------------------------------- #

# Prueba de incio sincronizado con tiempo x de dormir al inicar las tareas.
# Además comienzo de uso de biblioteca Tareas.py (Creada por Imanol Ayude Prieto)

# Inclusión de creación de un archivo CSV, simulando la comunicación con servidor:
# se quiere estimar cuanto tiempo se tarda en hacer esta creación, ya que se estima
# que esta sea mucho mayor que los periodos de la adquisición.
# Por lo que a lo mejor hay que dormir a las tareas de adquisición mientras se está
# comunicando o en este caso creando el archivo CSV


# ---------------------------------- Programa ---------------------------------- #

from asyncio import wait_for
import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
import max30100 # Biblioteca con la cual se utiliza en sensor MAX30100
import time
import Tareas

import csv

# ------------ Funciones que irán dentro de las tareas ------------ #

def CogerGuardarDatosPOX(a_ir, a_r):
        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo

    # ------------- Guardar datos en los arrays -------------#
    
        a_ir.append(infrarrojo)
        a_r.append(rojo)
                

def CogerGuardarDatosGSR(a_pox):
        global a
        a_pox.append(a)
        a = a + 1
        
def coms(a_ir,a_rojo, a_gsr):
        print ("Ciclo 1: ", a_ir )
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        print(a_ir)
        

# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    mx30 = max30100.MAX30100()
    mx30.enable_spo2()
    
    # Se crean objetos protegidos mediante manager
    mng = mp.Manager()
    y_Ir = mng.list()
    y_Rojo = mng.list()
    y_GSR = mng.list()
    
    #
    a=1
    #
    
    tiempo0 = time.time() # Tiempo inicial
    
    tarea1 = mp.Process(target = Tareas.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 1, 0.0117647, 0.008, CogerGuardarDatosPOX, y_Ir,y_Rojo))
    tarea2 = mp.Process(target = Tareas.Tarea_Periodica_Sensores_1Arr, args = (tiempo0, 2, 0.05, 0.01, CogerGuardarDatosGSR, y_GSR))
    tarea3 = mp.Process(target = Tareas.Tarea_Periodica_Sensores_3Arr, args = (tiempo0, 3, 60, 5, coms, y_Ir, y_Rojo, y_GSR))
    
    tarea1.start()
    tarea2.start()
    tarea3.start()
    
    tarea1.join()
    tarea2.join()
    tarea3.join()
    
    # print(y_Ir[2990:3000],len(y_Ir))
    # print(y_Rojo[2990:3000],len(y_Rojo))
    # print(y_GSR[590:600], len(y_GSR))
    
  
    
