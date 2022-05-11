#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 05 / 04 / 2022                      ##
##                                                             ## 
#################################################################

# Pruebas para lograr que se compartan variables entre 







#################################################################

import multiprocessing as mtp
import time
import max30100

fin = 0 

# --------------- función para obtener datos sensor POX --------------- #

def pox_coger_datos(Periodo, a_I, a_R,time_inicio):
        
    # Medición del tiempo en el que se lanza la tarea
    next_call = time.time() 
    time_inicio.append(next_call)
    print(time_inicio[0])
    # ------------- Parte cíclica de la tarea -------------#
    
    while 1:

        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo
        
        print ("------ Tarea 1 ------")
  
    # ------------- Guardar datos en los arrays -------------#
    
        a_I.append(infrarrojo)
        a_R.append(rojo)
        next_call = next_call + Periodo  # instante en el que finaliza la tarea 

    # ------------- Suspensión tarea hasta cumplir el periodo ------------- #   
            
        time.sleep(next_call - time.time())    # se suspende la tarea hasta 
        
        # -- Cada 500 datos se representa el tiempo tardado en recogerlos -- #
        
        if len(a_I) >= 6000:
            print(len(a_I))
        

# --------------- función para contar datos sensor POX --------------- #     (lo que será el GSR)

def GSR_coger_datos(periodo, a_gsr):
    hola = 0
    next_call2 = time.time() #############################################
    
    while 1:
        
        hola = hola + 1
        next_call2 = next_call2 + periodo*5 
        print('------------------- Tarea 2 ------------------- :', hola)
        a_gsr.append(hola)
        time.sleep(next_call2 - time.time())
        if len(a_gsr) >=1200:
            hola = 0
            
# --------------- función para borrar datos de los array --------------- #     (lo que será la subida de datos)            
            
def escribir_arrays (periodo, a_I, a_R, a_GSR, tiempo_inicio):

    ts = 0
    hola = time.time()
    
    while 1:
        
        # Parte cíclica de la tarea, dónde se presenta y se borran
        # los arryas gloables

        time.sleep(10 - ts - (hola-tiempo_inicio[0]))
        ts = time.time()  
        print("\n")
        print("------------------- TAREA 3 -------------------:", len(a_I))
        print(a_I)
        print(a_GSR)
        a_I[:] = []
        a_R[:] = []
        a_GSR[:] = []
        print(a_I)
        ts = time.time()-ts

# ---------------------------- MAIN ---------------------------- #
# Se inicializa el sensor Pulsioximetro

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# Se inicializan los arrays/buffer dónde se guardarán los datos recogidos por el sensor
mng = mtp.Manager()

y_Ir = mng.list()
y_Rojo = mng.list()
y_GSR = mng.list()

tiempo_inicio_POX = mng.list()

# Inicialización de variables características 

Periodo_POX = 0.01  # Periodo para la medición POX en SEGUNDOS

# Porgrama cíclico


Tarea_POX =mtp.Process(target = pox_coger_datos, args=(Periodo_POX, y_Ir, y_Rojo, tiempo_inicio_POX,))

Tarea_GSR = mtp.Process(target = GSR_coger_datos, args=(Periodo_POX, y_GSR,))

Tarea_PonerDatos = mtp.Process(target = escribir_arrays, args = (Periodo_POX,y_Ir, y_Rojo, y_GSR, tiempo_inicio_POX,))

Tarea_POX.start()

Tarea_GSR.start()
Tarea_PonerDatos.start()

Tarea_PonerDatos.join()
Tarea_POX.join()
Tarea_GSR.join()



