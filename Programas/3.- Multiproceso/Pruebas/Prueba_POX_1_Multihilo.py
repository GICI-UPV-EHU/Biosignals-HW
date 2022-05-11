
import threading as thr

#import multiprocessing as mtp
import time
import max30100

fin = 0 

# --------------- función para obtener datos sensor POX --------------- #

def pox_coger_datos(Periodo):

    # Se cogen los arrays globales, para poder introducir los valores
    # del sensor dentro de él
    
    global y_Ir
    global y_Rojo
 
    
    # Medición del tiempo en el que se lanza la tarea
    
    next_call = time.time()
    tiempo0 = time.time()
    
    # ------------- Parte cíclica de la tarea -------------#
    
    while 1:

        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo
        
        print ("------ Tarea 1 ------")
  
    # ------------- Guardar datos en los arrays -------------#
    
        y_Ir.append(infrarrojo)
        y_Rojo.append(rojo)
        next_call = next_call + Periodo  # instante en el que finaliza la tarea 

    # ------------- Suspensión tarea hasta cumplir el periodo ------------- #   
            
        time.sleep(next_call - time.time())    # se suspende la tarea hasta 
        
        # -- Cada 500 datos se representa el tiempo tardado en recogerlos -- #
        
        if len(y_Ir) >= 2000:
            tiempo1= time.time()
            print(len(y_Ir))
            print(tiempo1-tiempo0)

# si llega aqui significa que el programa ha fallado 
# por lo que se genera un flag de fin

    global fin
    fin = 1
        

# --------------- función para contar datos sensor POX --------------- #     (lo que será el GSR)

def contar_datos(periodo):
    next_call2 = time.time()
    hola = 0
    global fin
    while 1:
        hola = hola + 1
        next_call2 = next_call2 + periodo*5 
        print('------------------- Tarea 2 ------------------- :', hola)
        time.sleep(next_call2 - time.time())
        if hola == 400:
            hola = 0
            
# --------------- función para borrar datos de los array --------------- #     (lo que será la subida de datos)            
            
def escribir_arrays (periodo):
    
    ts = 0
    
    # Se cogen los arrays globales, para poder introducir los valores
    # del sensor dentro de él
    
    global y_Ir
    global y_Rojo
    
    while 1:
        
        # Parte cíclica de la tarea, dónde se presenta y se borran
        # los arryas gloables
        
        time.sleep(periodo*2000 -ts)
        ts = time.time()  
        print("\n")
        print("------------------- TAREA 3 -------------------\n", len(y_Ir))
        print(y_Ir)
        y_Ir.clear()
        y_Rojo.clear()
        ts = time.time()-ts

# ---------------------------- MAIN ---------------------------- #
# Se inicializa el sensor Pulsioximetro

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# Se inicializan los arrays/buffer dónde se guardarán los datos recogidos por el sensor

y_Ir, y_Rojo = [] , []

# Inicialización de variables características 

Periodo_POX = 0.01  # Periodo para la medición POX en SEGUNDOS

# Porgrama cíclico


Tarea_POX =thr.Thread(target = pox_coger_datos, args=(Periodo_POX,))

Tarea_contador = thr.Thread(target = contar_datos, args=(Periodo_POX,)) 

Tarea_PonerDatos = thr.Thread(target = escribir_arrays, args = (Periodo_POX,))

Tarea_POX.start()
Tarea_contador.start()
Tarea_PonerDatos.start()






