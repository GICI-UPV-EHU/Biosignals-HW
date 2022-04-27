import datetime as dt
from pyexpat.errors import XML_ERROR_TAG_MISMATCH
import matplotlib.pyplot as plt
import max30100
import time

Periodo =100.0 # el periodo establcido en MILISEGUNDOS (ms)
T_muestra = 1.0 # cada cuantos segundos se muestra una gráfica de muestras

i = 0
x_Tiempo, y_Ir, y_Rojo, tiempos = [] ,[] , [], []
Infrarojo=0.0
Rojo=0.0
tiempo=0.0

# inicialización del sensor max30100

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# función que se va a llamará periodicamente

def Coge_datos(Infrarojo, Rojo):
   
   # lectura de las medidas actuales
   mx30.read_sensor()
   Infrarojo = int(mx30.ir)
   Rojo = int (mx30.red)
   

   
# Main del programa 
t_ini1 = time.time()
while 1:
    t_asd = T_muestra/Periodo
    t_ini = time.time()
    while t_asd<=(T_muestra/Periodo):
        
        if  t_asd >= (T_muestra/Periodo):
            t_asd = 0 
            Coge_datos(Infrarojo, Rojo )
 
            # añadir la x (tiempo) y la y (medeida del sensor) a listas
   
            x_Tiempo.append(dt.datetime.now().strftime('%M:%S.%f')) # Esta hace que se retrase la adquisición de datos
   
            #x_Tiempo.append(i)
            y_Ir.append(Infrarojo)
            y_Rojo.append(Rojo)        

            
        t_asd = time.time()-t_ini
        
    t_act = time.time()
    if t_act-t_ini1>= 10.005:
 
        print(len(x_Tiempo))     
        x_Tiempo.clear()
        y_Rojo.clear()
        y_Ir.clear()

        print(t_act-t_ini1)
        t_ini1=time.time()




        


