import time
from multiprocessing import Event

def Tarea_Periodica_Sensores_3Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    while 1:
        for i in range(0, 5100): #######
            Funcion(array1, array2, arrayT)
            t_prueba=time.time()
            if (time.time()-next_time) > Plazo:
                error = error + 1
                print(" Abort:T", Identificador)
                if error == 5:
                    break
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            
            if len(array1) == 5100:
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

def Tarea_Periodica_Sensores_5Arr_Duerme_Ini (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT, array3, array2T):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio) + Periodo)
    next_time = time.time()
    error = 0
    while 1:
            print ("---------------- Tarea Coms -------------------")
            Funcion(array1, array2, arrayT, array3, array2T)
            t_prueba=time.time()
            if (time.time()-next_time) > Plazo:
            
                error = error + 1
                print(" Abort:T", Identificador)

                if error == 5:
                    break
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)