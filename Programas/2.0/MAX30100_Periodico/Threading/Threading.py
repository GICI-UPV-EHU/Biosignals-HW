import threading
import time

hola = 0
periodos = 1
periodo = 1

x,y = [],[]

def calculo_contador(periodo_s):
    
    tiempo_siguiente = time.time()
    time0 = time.time()
    
    global hola
    global x
    
    while len(x) != 10:
    
        tiempo_siguiente = tiempo_siguiente + periodo_s
        
        x.append(hola)
        print('Soy la tarea 1: ', hola)
        hola = hola +1
        
        time.sleep(tiempo_siguiente - time.time())

    print('Tarea 1 -> Array length: ', len(x))
    time1 = time.time()
    print(time1 - time0)
    

def calculo_contador2():
    
    tiempo_siguiente = time.time()
    time0 = time.time()
    
    global periodos
    global hola
    global y
    
    while len(y) != 5:
        
        tiempo_siguiente = tiempo_siguiente + periodo*2
        
        y.append(hola)
        print('Soy la tarea 2: ', hola)
        hola = hola +1
        
        time.sleep(tiempo_siguiente - time.time())

    print('Tarea 1 -> Array length: ', len(x))
    time1 = time.time()
    print(time1 - time0)
    
    
Tarea1 = threading.Thread(target= calculo_contador, args=(periodo,))
Tarea2 = threading.Thread(target= calculo_contador2)
Tarea1.start()
Tarea2.start()