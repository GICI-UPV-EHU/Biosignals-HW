#################################################################
##                                                             ##
##               USER  : IMANOL AYUDE PRIETO                   ##

##                 FECHA : 12 / 04 / 2022                      ##
##                                                             ## 
#################################################################


# ---------------------------------- Enunciado ---------------------------------- #

# Se ha visto que la sincronización de estas tareas no es buena, por lo que en 
# esta primera prueba, se va a proceder a crear un inicio sincronizado de todas 
# las tareas


# ---------------------------------- Programa ---------------------------------- #


import time
import multiprocessing as mp
import max30100

def Tarea_Periodica(tiempo0, periodo, plazo):
    next_time = tiempo0
    
    y_Ir, y_Rojo = [], []
    error = 0
    while len(y_Ir) <4000:
        rojo = 0
        infrarrojo = 0
        mx30.read_sensor()
        infrarrojo = mx30.ir  # se recoge el valor del led infrarrojo
        rojo = mx30.red       # se recoge el valor del led rojo
        
        #print ("------ Tarea 1 ------", len(y_Ir),"    ", len(y_Rojo))
  
    # ------------- Guardar datos en los arrays -------------#
    
        y_Ir.append(infrarrojo)
        y_Rojo.append(rojo)
        if (time.time()-next_time)>= plazo:
            error = error +1
            print("Aborto - T1 - ", error)
            next_time = next_time + periodo
            time.sleep(next_time - time.time()) 
            if error == 5:
                break
        else:
            if len(y_Ir)< 4000:
                next_time = next_time + periodo
                time.sleep(next_time - time.time())   
    print("Tarea 1", time.time()-tiempo0 ,"Longitud array", len(y_Ir))

def Tarea_Periodica2(tiempo0, periodo, plazo):
    next_time = tiempo0
 
    y_Ir, y_Rojo = [], []
    error = 0
    infrarrojo = 0
    rojo = 0
    while len(y_Ir) < 800:
            
        #print ("------ Tarea 2 ------", len(y_Ir),"    ", len(y_Rojo))
  
    # ------------- Guardar datos en los arrays -------------#
        infrarrojo = infrarrojo + 1
        rojo = rojo + 1
        y_Ir.append(infrarrojo)
        y_Rojo.append(rojo)
        if (time.time()-next_time)>= plazo:
            error = error +1
            print("Aborto - T2 - ", error)
            next_time = next_time + periodo
            time.sleep(next_time - time.time()) 
            if error == 3:
                break
        else:
            if len(y_Ir)< 800:
                next_time = next_time + periodo
                time.sleep(next_time - time.time())   
        
    print("Tarea 2", time.time()-tiempo0, "Longitud array", len(y_Ir))
    
def Tarea_Periodica3(tiempo0, periodo, plazo):

    ts = tiempo0 - time.time()
    while 1:
        time.sleep(periodo+ts)
        ts = time.time()
        print ("--------- Tarea 3 ------------")
        ts = time.time()- ts    
        
    print(time.time()-tiempo0)


# --------------------------- Programa Principal --------------------------- #

mx30 = max30100.MAX30100()
mx30.enable_spo2()

tiempo_inicio = time.time()+1
tare1 = mp.Process(target= Tarea_Periodica,  args=(tiempo_inicio, 0.01, 0.008))
tare2 = mp.Process(target= Tarea_Periodica2, args=(tiempo_inicio, 0.05, 0.002))
tare3 = mp.Process(target= Tarea_Periodica3, args=(tiempo_inicio, 40  , 0.05 ))
tare1.start()
tare2.start()
tare3.start()

# ------------------------------ Conclusión -----------------------------#
# a grandes rasgos se ha logrado que se sincronicen las 3 tareas periodicas
# pero con una trampa, alargando el primero de los periodos. Esto hace que 
# no sea muy fiable el código

# se va a porbar en el siguiente código, a dormir todas las tareas, un
# timepo espécifico, para que depués todas ellas, comiencen en el mismo instante

