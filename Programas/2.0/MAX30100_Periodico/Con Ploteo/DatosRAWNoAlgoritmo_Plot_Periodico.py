import datetime as dt
import matplotlib.pyplot as plt
import max30100
import time

Periodo = 100.0 # el periodo establcido en MILISEGUNDOS (ms)
T_muestra = 1.0 # cada cuantos segundos se muestra una gráfica de muestras

i=0

# creación de la ventana dónde se va a crear la gráfica
fig = plt.figure()

# creación de la gráfica dentro de la figura

graf_ir = fig.add_subplot(2, 1, 1)
graf_rojo = fig.add_subplot(2, 1, 2)
x_Tiempo, y_Ir, y_Rojo = [] ,[] , []

# inicialización del sensor max30100

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# función que se va a llamar periodicamente

def animate( i, x_Tiempo, y_Ir, y_Rojo):
   

   # lectura de las medidas actuales
   mx30.read_sensor()
   Infrarojo = int(mx30.ir)
   Rojo = int (mx30.red)
   
   # añadir la x (tiempo) y la y (medeida del sensor) a listas
   
   #x_Tiempo.append(dt.datetime.now().strftime('%M:%S.%f')) # Esta hace que se retrase la adquisición de datos
   
   x_Tiempo.append(i)
   y_Ir.append(Infrarojo)
   y_Rojo.append(Rojo)
   
   # Comporbación de que se añaden los valores a los arrays
   #print(x_Tiempo)
   #print(y_Ir)
   #print(y_Rojo)
   
   # se limitan los arryas hasta 50 elementos => los que se verán en la gráfica

   
   # Comprobación de que se recorta el array al valor indicado
   #print(x_Tiempo)
   #print(y_Ir)
   #print(y_Rojo)
   
   # formato de la gráfica  


   
# función que llamará periodicamente a 'animate'

while 1:
    t_ini = time.time()
    t_duracion_entero=0
    t_asd = 0
    while t_duracion_entero<T_muestra:
        
        if t_asd == 0 or t_asd > (T_muestra/Periodo):
            t_asd = 0 
            t_ini1= time.time()
            animate(i, x_Tiempo, y_Ir, y_Rojo)
            i=i+1
            x_Tiempo = x_Tiempo[-100:]
            y_Ir = y_Ir[-100:]
            y_Rojo = y_Rojo[-100:]
            print(x_Tiempo)
        t_asd = time.time()-t_ini1
        t_duracion_entero = time.time()-t_ini
    print('ok')
            
    graf_ir.clear()
    graf_rojo.clear()
   
    graf_ir.title.set_text('Medidas infrarojas')
    graf_rojo.title.set_text('Medidas led rojo')
   
    graf_ir.tick_params(labelrotation =45)
    graf_rojo.tick_params(labelrotation = 45)
    graf_ir.plot(x_Tiempo, y_Ir, linewidth = 2, color = 'r')
    graf_rojo.plot(x_Tiempo, y_Rojo, linewidth =2, color = 'b')       
    plt.draw()   
    plt.pause(0.01)
    graf_ir.clear()
    graf_rojo.clear()
    
    print('ok2')


        


