#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 02 / 04 / 2022                      ##
##                                                             ## 
#################################################################


# ---------------------------------- Enunciado ---------------------------------- #

# Tras lanzar el primer programa (Prueba_POX_2) en la raspberry 
# py 0, se ha visto que el funcionamiento del threading no 
# funciona correctamente, ya que solo usa uno de los 4 procesadores

# Por lo que en este programa se va a usar en vez del THREADING, 
# el MULTIPROCESSING, lo que debería de usar al máximo todos los
# procesadores de la placa.

# No es complicado el cambio, ya que sigue la misma estrucutra de 
# programación. Solo es necesario cambiar la bilbioteca, y dónde
# había un Threading.Thread, cambairlo por un
# Multiprocessing.Process


# ---------------------------------- Programa ---------------------------------- #
  
#import threading as thr
import multiprocessing as mtp
import time
import max30100
import datetime as dt

fin = 0 
# --------- función para obtener datos sensor POX --------- #

def pox_coger_datos(a_ir, a_ro, a_t, Periodo):
    
    i = 0
 
    next_call = time.time()
    tiempo0 = time.time()
    while len(a_ir) < 6000:
      
        i = i+1

        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo
        tiempo = dt.datetime.now().strftime('%M:%S.%f') # se guarda el instante de toma de datos
        print (len(a_ir))

    
    
    # ------------- Guardar datos en los arrays -------------#
    
        a_ir.append(infrarrojo)
        a_ro.append(rojo)
        a_t.append(tiempo)
        next_call = next_call + Periodo  # instante en el que finaliza la tarea 

    # ------------- Suspensión tarea hasta cumplir el periodo ------------- #           
        time.sleep(next_call - time.time())    # se suspende la tarea hasta que llege al periodo
        
    global fin
    fin = 1
    tiempo1= time.time()
    print(len(y_Ir))
    print(tiempo1-tiempo0)
    

def contar_datos(periodo):
    next_call2 = time.time()
    hola = 0
    global fin
    while hola != 1200 and fin == 0:
        hola = hola + 1
        next_call2 = next_call2 + periodo*5 
        print('Tarea 2:', hola)
        time.sleep(next_call2 - time.time())

    

# ---------------------------- MAIN ---------------------------- #
# Se inicializa el sensor Pulsioximetro

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# Se inicializan los arrays/buffer dónde se guardarán los datos recogidos por el sensor

x_Tiempo, y_Ir, y_Rojo = [] ,[] , []

# Inicialización de variables características 

Periodo_POX = 0.01  # Periodo para la medición POX en SEGUNDOS

#Tarea_POX =thr.Thread(target = pox_coger_datos, args=(y_Ir, y_Rojo, x_Tiempo, Periodo_POX,))
#Tarea_contador = thr.Thread(target = contar_datos, args=(Periodo_POX,))

Tarea_POX =mtp.Process(target = pox_coger_datos, args=(y_Ir, y_Rojo, x_Tiempo, Periodo_POX,))
Tarea_contador = mtp.Process(target = contar_datos, args=(Periodo_POX,)) 
    
Tarea_POX.start()
Tarea_contador.start()


# ---------------------------------- Conclusión ---------------------------------- #

# Tras ejecutar el código se ha visto, que el array no pasa de una tarea a otra 
# como si ocurría con los Threads. Por lo que es necesario buscar el modo de llevar
# a cabo esta compartición de objetos/arrys 
# (OBJETOS PROTEGIDOS, van a ser leidos/escritos por más de un proceso)


