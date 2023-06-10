import connect_bbdd
# utilizamos time para crear buffer de 5 min antes de escribirlo en BBDD
import time
# necesitamos introducir timestamps en la BBDD para saber los momentos de las lecturas
from datetime import datetime, timezone
# importamos pytz porque datetime sólo trabaja con UTC y necesitamos hacer la conversión
import pytz
# Obtenemos rojo, infrarrojo y cálculo de valores
import obtener_valores
# Leemos ADC
#import ADC
import psycopg2
import sys
# Trabajaremos con multiproceso en el momento de generar el buffer
# Esto lo hacemos para leer paralelamente desde el ADC y el max30102
# Además utilizaremos multiproceso también para generar el buffer y escribir en la base de datos de forma concurrente.
import multiprocessing as mpr
from multiprocessing import Process, Queue


import BiblioTareasPeriodicas

### Introducimos una rutina previa para obtener un ID único por placa, aprovechando que cada dirección MAC de la WLAN es única por dispositivo
### Esto nos sirve como identificativo único de dispositivo y por tanto de usuario para poder hacer luego las Insert en la BBDD
import subprocess

def generar_buffer(q):

    # Obtenemos el ID, único por dispositivo
    
    ### Obtenemos valores rojo / infrarrojo en un procesador dedicado
    # Dado que disponemos de varios procesadores, vamos a aprovechar el multiproceso
    # dedicando uno de ellos a las lecturas de POX y el otro al ADC. Con los datos de ambos, los introduciremos en una cola FIFO (Queue)


        # Tenemos que usar pytz para sacar la fecha adecuada ya que datetime sólo trabaja con UTC.
    fecha = datetime.now()
        #fecha = '02-02-2022 00:00:00.000'
        # Hay que crear la cola FIFO con 6 datos: 
        # Usuario, rojo, infrarrojo, Pulso_SPO2, sudoracion, fecha
        # De momento introducimos sudoracion como valor ficticio según el valor ficticio obtenido con el ADC
        # El pulso y spo2 corresponden realmente a los valores de rojo e infrarrojo. Se hace media de 100 valores de cada rojo e infrarrojo en cada línea
        
        # Sirviéndonos del multiproceso, utilizamos un pool de 2 procesos para obtener valores concurrentemente del max30102 y el ADC.
    pool = mpr.Pool(processes=1)
                
    resultado_async_max30102 = pool.apply_async(obtener_valores.coger_datos).get()
        #resultado_async_adc = pool.apply_async(ADC.leer_adc).get()
                       
    datos_sensores = [ fecha, resultado_async_max30102[0], resultado_async_max30102[1]]
        # close() llama a destruir el pool y join() espera a los procesos trabajadores.
    pool.close()
    pool.join()
        
        ### Llenamos la cola FIFO con los datos de los sensores
    q.put(datos_sensores)    
             
### Rutina principal
def main():
    
    q = Queue()
    
    #### Llenamos la cola FIFO
    #llenar_buffer = Process(target=generar_buffer, args=(q,))     
       
    t0 = time.time()
    llenar_buffer = Process(target=BiblioTareasPeriodicas.Tarea_Periodica_Sensores_1Arr, args =(t0, 1, 0.5,0.5, generar_buffer, q))
    #### Vaciado de la cola FIFO 
    envio_bbdd = Process(target=connect_bbdd.insertar_sensores_bbdd_batch_queue, args=(q,))
    llenar_buffer.start()
    envio_bbdd.start()
       
  
    llenar_buffer.join()
    envio_bbdd.join()
    
## Ejecución
if __name__ == "__main__":
    main()
    
