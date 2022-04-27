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
import max30100 # Biblioteca con la cual se utiliza en sensor MAX30100
import time
import Tareas2
import csv

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
        a_t.append(time.strftime('%d, %m, %Y --> %H:%M:%S', time.localtime()))

def CogerGuardarDatosGSR(a_pox, a_t):
        global a
        a_pox.append(a)
        a_t.append(time.strftime('%d, %m, %Y --> %H:%M:%S', time.localtime()))
        a = a + 1
        
def coms(a_ir,a_rojo, a_t_P, a_gsr, a_t_G):
        print ("Ciclo 1: " , len(a_ir))
        with open('POX.csv', "w") as POX_CSV:
                w = csv.writer(POX_CSV)
                for i in range(len(a_ir)):
                        w.writerow([a_ir[i], a_rojo[i], a_t_P[i]])
                        
        with open('GSR.csv', "w") as GSR_CSV:
                w = csv.writer(GSR_CSV)
                for i in range(len(a_gsr)):
                        w.writerow([a_gsr[i], a_t_G[i]])
                                                
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        print("Limpios: ", len(a_ir))
        print(" \n")
        print(" \n")

        

# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    mx30 = max30100.MAX30100()
    mx30.enable_spo2()
    
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
    
    tarea1 = mp.Process(target = Tareas2.Tarea_Periodica_Sensores_3Arr, args = (tiempo0, 1, 0.0117647, 0.011, CogerGuardarDatosPOX, y_Ir,y_Rojo, y_t_POX))
    tarea2 = mp.Process(target = Tareas2.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 2, 0.05, 0.01, CogerGuardarDatosGSR, y_GSR, y_t_GSR))
    tarea3 = mp.Process(target = Tareas2.Tarea_Periodica_Sensores_5Arr_Duerme_Ini, args = (tiempo0, 3, 60, 60, coms, y_Ir, y_Rojo, y_t_POX, y_GSR, y_t_GSR))
    
    tarea1.start()
    tarea2.start()
    tarea3.start()
    
    tarea1.join()
    tarea2.join()
    tarea3.join()
    
    
    ###################################################
    #                      CONCLUSION                 #
    
# como era de preveer, la tercera de las tareastarda más de
# lo que se quisiera, por lo que a la hora de que el programa
# se ejecute ciclicamente, no funcionaría.
# Además, se ha visto que mientras la tarea 3 se está ejecutando
# las demás tareas siguen ejecutandose, lo que hace que los
# la cantidad de datos que se guardan en los archivos CSV no sea
# estable.
  #                  SIGUIENTE PRUEBA
# se podría arreglar, haciendo que la tercera de las tareas fuera 
# esporadica, y se activara solo cuando la tarea1 y la 2 hayan 
# hecho sus 60 s de adquisición de datos.