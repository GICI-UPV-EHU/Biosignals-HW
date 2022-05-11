import time
import csv

def Tarea_Periodica_Sensores_3Arr (tiempo_inicio, Identificador, Periodo, Plazo, Funcion, array1, array2, arrayT):
    
    a_tmax = []
    
    time.sleep(0.1 - (time.time() - tiempo_inicio))
    next_time = time.time()
    error = 0
    for i in range(0, 3000): #######
        
        t_prueba=time.time()
        Funcion(array1, array2, arrayT)
        
        if (time.time()-next_time) > Plazo:
            error = error + 1
            if error == 5:
                break
        next_time = next_time + Periodo
        a_tmax.append(time.time()-t_prueba)
        time.sleep(next_time - time.time())
            
    print("Tiempo Tardado en la Tarea ", Identificador," = ", time.time()-tiempo_inicio-0.1)
    
    t_max = 0.0
    
    with open ('/home/pi/Desktop/GSR.csv', "w") as GSR_CSV:
        w = csv.writer(GSR_CSV)
        for i in range(len(a_tmax)):
            w.writerow([a_tmax[i]])
            if a_tmax[i] > t_max:
                t_max = a_tmax[i]
    
    print("El mayor tiepo ha sido: ", t_max)
    
