

# Se añade un cambio en la tarea encargada de la comunicación
# procurando que esta tarea le el array que le viene desde las 
# otras dos tareas, y después la parte de creación del CSV, 
# hacerla con varaibles internas

from queue import Queue
from time import time, sleep
from multiprocessing import Event

    

def Tarea_Periodica_Sensores_3Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    while 1:
        for i in range(0, 3000): #######
            Funcion(array1, array2, arrayT)
            t_prueba=time.time()
            if (time.time()-next_time) > Plazo:
                error = error + 1
                print(" Abort:T", Identificador)
                if error == 5:
                    break
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            
            if len(array1) == 3000:
                print ("---------------- Tarea POX  -------------------")
                print("Tarea ", Identificador, ": ", len(array1))
        print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)
        
    
def Tarea_Periodica_Sensores_2Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, arrayT):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    while 1:
        for i in range(0, 1200): #################
            Funcion(array1, arrayT)
            t_prueba=time.time()
            if (time.time()-next_time) > Plazo:
                
                error = error + 1
                print(" Abort:T", Identificador)
                if error == 5:
                    break
            
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            
            if len(array1) == 1200:
                print ("---------------- Tarea GSR  -------------------")
                print("Tarea ", Identificador, ": ", len(array1))
        print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)

def Tarea_Periodica_Sensores_1Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, Queue):
    
    sleep(0.1 - (time() - tiempo_inicio))
    next_time = time()
    error = 0
    i = 0
    while 1:
            i = i + 1
            Funcion(Queue)
            # if (time()-next_time) > Plazo:
            #     print("Fuera de plazo real")
            #     break

            # if i == 100:
            #     print ("---------------- Tarea POX  -------------------")
            #     print("Tiempo Tardado en la Tarea ", Identificador," = ", time()-tiempo_inicio-0.1)
            #     i = 0
            next_time = next_time + Periodo
            try:
                sleep(next_time - time())  
            except(Exception):
                print("Fuera de plazo falso")
                break
            # if len(Queue) == 50:
            #     print ("---------------- Tarea GSR  -------------------")
            #     print("Tarea ", Identificador, ": ", len(Queue))






def Tarea_Periodica_Sensores_5Arr_Duerme_Ini (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT, array3, array2T):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio) + Periodo)
    next_time = time.time()
    error = 0
    while 1:
            t_prueba=time.time()
            ar1 = array1[:]
            ar2 = array2[:]
            arT1 = arrayT[:]
            ar3 = array3[:]
            arT2 = array2T[:]
            array1[:] = []
            array2[:] = []
            arrayT[:] = []
            array3[:] = []
            array2T[:] = []

            print ("---------------- Tarea Coms -------------------")
            Funcion(ar1, ar2, arT1, ar3, arT2)
            if (time.time()-next_time) > Plazo:
            
                error = error + 1
                print(" Abort:T", Identificador)

                if error == 5:
                    break
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-t_prueba)
