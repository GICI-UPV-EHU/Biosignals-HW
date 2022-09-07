#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 12 / 05 / 2022                      ##
##                                                             ## 
#################################################################

# ---------------------------------- Enunciado ---------------------------------- #

# Probar a ver si se logra resolver que las tres tareas periodicas se sincronicen
# correctamente, ya que el tiempo que tarda la tercera de llas peta las demás en 
# los siguientes ciclos

''' 
Se cambia el sensor Max30100 por el max 30102. En el cual la biblioteca de Python está bien
creada lo que permite una mejor organización de código y se supone que por ello, mejor optimización
'''

# ---------------------------------- Programa ---------------------------------- #

import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
import max30102 # Biblioteca con la cual se utiliza en sensor MAX30100
from datetime import datetime
import time
import BiblioTareasPeriodicas
import csv

# ------------ Funciones que irán dentro de las tareas ------------ #

def CogerGuardarDatosPOX(a_ir, a_r, a_t):
        a_t.append(datetime.now().strftime('%M:%S.%f'))
        rojo = 0
        infrarrojo = 0
        
        rojo, infrarrojo= mx30.read_fifo  # se recoge el valor del led infrarrojo

    # ------------- Guardar datos en los arrays -------------#
    
        a_ir.append(infrarrojo)
        a_r.append(rojo)
        #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))


def CogerGuardarDatosGSR(a_pox, a_t):
        global a
        a_pox.append(a)
        #a_t.append(time.strftime('%d/%m - %H:%M:%S.%f', time.localtime()))
        a_t.append(datetime.now().strftime('%M:%S.%f'))
        a = a + 1
        
def coms(a_ir,a_rojo, a_t_P, a_gsr, a_t_G):
        print ("Infrarrojo: " , len(a_ir), "Rojo: ", len(a_gsr))
        
        with open('/home/pi/Desktop/Data/POX.csv', 'a+', newline='') as POX_CSV:
                w = csv.writer(POX_CSV)
                for i in range(len(a_ir)):
                        w.writerow([a_ir[i], a_rojo[i], a_t_P[i]])
                        
        with open('/home/pi/Desktop/Data/GSR.csv', "a+", newline = '') as GSR_CSV:
                w = csv.writer(GSR_CSV)
                for i in range(len(a_gsr)):
                        w.writerow([a_gsr[i], a_t_G[i]])
                                                
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        a_t_P[:] = []
        a_t_G[:] = []
        print("Limpios: ", len(a_ir))
        print(" \n")
        print(" \n")

        

# ------------------ Programa Principal -------------------- #

if __name__ == "__main__":
    
    mx30 = max30102.MAX30102()
    
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
    tarea3 = mp.Process(target = BiblioTareasPeriodicas.Tarea_Periodica_Sensores_5Arr_Duerme_Ini, args = (tiempo0, 3, 30, 30, coms, y_Ir, y_Rojo, y_t_POX, y_GSR, y_t_GSR))
    
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