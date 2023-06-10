import time

def Tarea_Periodica_Sensores_2Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    #while 1:
    for i in range(0, 5100):
        Funcion(array1, array2)
        t_prueba=time.time()
        if (time.time()-next_time) > Plazo:
            
            error = error + 1
            print(" Abortada : Tarea ", Identificador)
            if error == 5:
                break
        next_time = next_time + Periodo
        if i != 5099:
            time.sleep(next_time - time.time())
        else:
            print("Tarea ", Identificador, ": ", len(array1))
            
    print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)
    
def Tarea_Periodica_Sensores_1Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    #while 1:
    for i in range(0, 1200):
        Funcion(array1)
        t_prueba=time.time()
        if (time.time()-next_time) > Plazo:
            
            error = error + 1
            print(" Abortada: Tarea ", Identificador)
            if error == 5:
                break
            
        next_time = next_time + Periodo
        if i != 1199:
            time.sleep(next_time - time.time())
        else:
            print("Tarea ", Identificador, ": ", len(array1))
            
    print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)

def Tarea_Periodica_Sensores_3Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, array3):
    
    time.sleep(0.1 - (time.time() - tiempo_inicio) + Periodo)
    print("############################################")
    next_time = time.time()
    error = 0
    #while 1:
    for i in range(0,1):
        Funcion(array1, array2, array3)
        t_prueba=time.time()
        if (time.time()-next_time) > Plazo:
            
            error = error + 1
            print(" Abortada : Tarea ", Identificador)

            if error == 5:
                break
        next_time = next_time + Periodo
        if i!=0:
            time.sleep(next_time - time.time())
    print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)