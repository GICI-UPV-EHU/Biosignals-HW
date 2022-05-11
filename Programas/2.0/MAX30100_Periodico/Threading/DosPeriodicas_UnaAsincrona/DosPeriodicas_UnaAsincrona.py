            #################################################################
            ##                                                             ##
            ##               USER  : IMANOL AYUDE PRIETO                   ##

            ##                 FECHA : 26 / 04 / 2022                      ##
            ##                                                             ## 
            #################################################################

# ---------------------------------- Enunciado ---------------------------------- #

# Debido a que no se puede llevar a cabo la sincronización de las tres tareas periodicas
# se ha decidido optar por porbar a que la tarea de comunicación sea asincrona, es decir
# que no va a tener un periodo ni va a estar limitada por ningún plazo.

# La tarea se activará cuando las dos tareas de adquisición de datos hayan medido los datos
# que corresponden a un minuto. Mientras esta tarea esté activa, las otras dos tareas periodicas
# estarán esperando a que la de comunicación acabe.

# Para llevar a cabo esta pausa en las tareas periodicas, se usarán la clase evento de la
# biblioteca multiprocessing, que funcionan como un semáforo binario, por lo que se podrá
# generar pausas a la espera de que se la haga un signal a un semáforo

# --------------------- Eventos ------------------------- #

#   evento.clear()  --> pone el semáforo a 0 
#   evento.set()    --> pone el semáforo a 1
#   evento.is_set() --> espera hasta que el semáforo/evento esté a 1


# ---------------------------------------------- Programa ---------------------------------------------- #

# -------------------------- Inlusión de las Bibliotecas que van a ser usadas -------------------------- #


import multiprocessing as mp # Biblioteca que se encarga de generar procesos (Tareas)
import max30100 # Biblioteca con la cual se utiliza en sensor MAX30100
from datetime import datetime # Biblioteca que ofrece la posibilidad de tener tiempo actual en Minutos:segundos,milisegundos

import time # Se usará para medir tiempos relativos 
import TareasPeriodicas_Asincronas  # Biblioteca dónde se encuntran las Tareas necesarias
import csv  


# -------------------------------- Funciones que irán dentro de las tareas -------------------------------- #

def CogerGuardarDatosPOX(a_ir, a_r, a_t):
        a_t.append(datetime.now().strftime('%M:%S.%f'))
        
        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo

    # ------------- Guardar datos en los arrays -------------#
        a_ir.append(infrarrojo)
        a_r.append(rojo)


def CogerGuardarDatosGSR(a_pox, a_t):
        global a
        a_pox.append(a)
        a_t.append(datetime.now().strftime('%M:%S.%f'))
        a = a + 1
        
def coms(a_ir,a_rojo, a_t_P, a_gsr, a_t_G):
        print ("Ciclo 1: " , len(a_ir))

        # ------- Creación y Escritura de CSV's ------- #

        with open('/home/pi/Desktop/Data/POX.csv', "w") as POX_CSV:
                w = csv.writer(POX_CSV)
                for i in range(len(a_ir)):
                        w.writerow([a_ir[i], a_rojo[i], a_t_P[i]])
                        
        with open('/home/pi/Desktop/Data/GSR.csv', "w") as GSR_CSV:
                w = csv.writer(GSR_CSV)
                for i in range(len(a_gsr)):
                        w.writerow([a_gsr[i], a_t_G[i]])
        
        # ------- Se borra la info de los arrays ------- #
                                                
        a_ir[:] = []
        a_rojo[:] = []
        a_gsr[:] = []
        print("Limpios: ", len(a_ir))
        print(" \n")
        print(" \n")

        

# ------------------------------------------- Programa Principal ------------------------------------------ #

if __name__ == "__main__":

    # -- Se crea el objeto mx30 y se habilata la medida SPO2 que activa el led infrarojo -- #
    
    mx30 = max30100.MAX30100()
    mx30.enable_spo2()
    
    # -------------------- Se crean objetos protegidos mediante manager ------------------- #

    mng = mp.Manager()   

    # ------- Arrays para el sensor POX ------- #

    y_Ir = mng.list()              # Array de medidas infrarrojas
    y_Rojo = mng.list()            # Array de medidas rojas
    y_t_POX = mng.list()           # Array para los tiempos de medida

    # ------- Arrays para el sensor GSR ------- #
    
    y_GSR = mng.list()             # Array de medidas GSR
    y_t_GSR = mng.list()           # Array para los tiempos de medida
    
    
    
    # -------------------------- Para que haga algo la tarea GSR -------------------------- #
    a=1
    #
    
    # -------------- Creación y asignación de valores inciales de los eventos ------------- #

    Flag_POX = mp.Event()
    Flag_GSR = mp.Event()
    Flag_COMS = mp.Event()

    Flag_GSR.clear()            # Se pone a 0 para que la Tarea1 pueda ejecutarse y la Tarea3 se bloquee
    Flag_POX.clear()            # Se pone a 0 para que la Tarea2 pueda ejecutarse y la Tarea3 se bloquee
    Flag_COMS.set()             # Se pone a 1 para que la Tarea1 y 2 puedan ejecutarse 

    # ------------- Se establece un tiempo inical común para todas las tareas ------------- #
    
    tiempo0 = time.time() # Tiempo inicial

    # ------------ Se crean las tres tareas con todos los parametros necesarios ----------- #
    
    tarea1 = mp.Process(target = TareasPeriodicas_Asincronas.Tarea_Periodica_Sensores_3Arr, args = (tiempo0, 1, 0.01666667, 0.015, CogerGuardarDatosPOX, y_Ir,y_Rojo, y_t_POX, Flag_POX, Flag_COMS))
    tarea2 = mp.Process(target = TareasPeriodicas_Asincronas.Tarea_Periodica_Sensores_2Arr, args = (tiempo0, 2, 0.05, 0.012, CogerGuardarDatosGSR, y_GSR, y_t_GSR,Flag_GSR, Flag_COMS))
    tarea3 = mp.Process(target = TareasPeriodicas_Asincronas.Tarea_Asincrona, args = (tiempo0, 3, 60, 60, coms, y_Ir, y_Rojo, y_t_POX, y_GSR, y_t_GSR, Flag_COMS, Flag_POX, Flag_GSR))
    
    # ------------------------ Se da comienzo a todas las tareas -------------------------- #

    tarea1.start()
    tarea2.start()
    tarea3.start()

    tarea1.join()
    tarea2.join()
    tarea3.join()
    
#####################################################################################################
# ------------------------------------------- CONCLUSIÓN ------------------------------------------ #

# Se hacen medidas del tiempo que el usuario quiera, cada ciclo de medición se activa la tarea de coms
# la cual se ejecuta sin que las otras dos tareas se ejecuten. Cuando esta acabe, las tareas de 
# medición se ejecturán y volverán a medir el tiempo establecido

# ---------------------------------------- Siguiente Prueba --------------------------------------- #

# lograr reducir el tiempo de comunicación para que las tres tareas se puedan paralelizar, y que las
# tareas de medición puendan ser periodicas, y den datos continuamente