# -------------------------------- Eventos ------------------------------ #

#   evento.clear()  --> pone el semáforo a 0 
#   evento.set()    --> pone el semáforo a 1
#   evento.is_set() --> espera hasta que el semáforo/evento esté a 1i





import time


def Tarea_Periodica_Sensores_3Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT, f_POX, f_COMS):
    fin = 0

    time.sleep(5 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    while 1:
        time0 = time.time()
        while f_POX.is_set():
            f_COMS.wait()
        
        time1 = time.time()
        next_time= next_time + time1-time0
        
        for i in range(0, 300): #######
            Funcion(array1, array2, arrayT)
            t_prueba=time.time()
            if (time.time()-next_time) > Plazo:
                error = error + 1
                print(" Abort:T", Identificador)
                if error == 5:
                    break
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            
            if len(array1) == 300:
                print ("---------------- Tarea POX  -------------------")
                print("Tarea ", Identificador, ": ", len(array1))

        print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time() - time1)
        f_POX.set()
        
    
def Tarea_Periodica_Sensores_2Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, arrayT, f_GSR, f_COMS):
    
    time.sleep(5 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    while 1:
        time0 = time.time()
        while f_GSR.is_set():
            f_COMS.wait()

        time1 = time.time()
        next_time= next_time + time1 - time0

        for i in range(0, 100): #################
            Funcion(array1, arrayT)
            t_prueba=time.time()
            if (time.time()-next_time) > Plazo:
                
                error = error + 1
                print(" Abort:T", Identificador)
                if error == 5:
                    break
            
            next_time = next_time + Periodo
            time.sleep(next_time - time.time())
            
            if len(array1) == 100:
                print ("---------------- Tarea GSR  -------------------")
                print("Tarea ", Identificador, ": ", len(array1))
        print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-time1)

        f_GSR.set()

def Tarea_Asincrona (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT, array3, array2T, f_COMS, f_POX, f_GSR):
    
#     time.sleep(0.1 - (time.time() - tiempo_inicio) + Periodo)
#     next_time = time.time()
#     error = 0
    while 1:
            f_POX.wait()
            f_GSR.wait()
            f_COMS.clear()
            t_prueba=time.time()
            print ("---------------- Tarea Coms -------------------")
            Funcion(array1, array2, arrayT, array3, array2T)

            print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-t_prueba)
            
            f_POX.clear()
            f_GSR.clear()
            f_COMS.set()