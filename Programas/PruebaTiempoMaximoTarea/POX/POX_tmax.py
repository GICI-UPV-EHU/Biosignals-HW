#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 27 / 04 / 2022                      ##
##                                                             ## 
#################################################################

# ---------------------------------- Enunciado ---------------------------------- #

# Pureba de tiempo máximo que tarda en ejecutarse la tarea


# ---------------------------------- Programa ---------------------------------- #

import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
import max30100 # Biblioteca con la cual se utiliza en sensor MAX30100
from datetime import datetime
import time
import TareasPruebaPOX

# ------------ Funciones que irán dentro de las tareas ------------ #

def CogerGuardarDatosPOX(a_ir, a_r, a_t):
        
        
        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo

    # ------------- Guardar datos en los arrays -------------#
    
        a_ir.append(infrarrojo)
        a_r.append(rojo)
        a_t.append(datetime.now().strftime('%M:%S.%f'))


# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    mx30 = max30100.MAX30100()
    mx30.enable_spo2()
    
    # Se crean objetos protegidos mediante manager
    mng = mp.Manager()
    y_Ir = mng.list()
    y_Rojo = mng.list()
    y_t_POX = mng.list()
 
    
    tiempo0 = time.time() # Tiempo inicial
    
    tarea1 = mp.Process(target = TareasPruebaPOX.Tarea_Periodica_Sensores_3Arr, args = (tiempo0, 1, 0.02, 0.015, CogerGuardarDatosPOX, y_Ir,y_Rojo, y_t_POX))
    
    tarea1.start()
    
    tarea1.join()
    
    