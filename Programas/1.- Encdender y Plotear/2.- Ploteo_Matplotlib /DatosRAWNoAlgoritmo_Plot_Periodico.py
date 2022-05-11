# --------------------------- Inclusión de Librerías --------------------------- #

import datetime as dt

# Instalar (Matplotlib / Numpy (pip3 install -U numpy) 
# Instalar --> sudo apt-get install libatlas-base-dev

import matplotlib.pyplot as plt

import max30100
import time

# ---------------- Variables usadas para el cálculo del periodo ---------------- #

n_muestra = 65.0          # Nº de muestras en T_muestras
T_muestra = 1.0           # Cada cuantos segundos se muestra una gráfica

i=0         # Varaible que hará de tiempo (se irá aumentando en 1 cada medida)

# ----------- Creación de la ventana dónde se va a crear la gráfica  ----------- #

fig = plt.figure()

# ----------------- Creación de la gráfica dentro de la figura ----------------- #

graf_ir = fig.add_subplot(2, 1, 1)
graf_rojo = fig.add_subplot(2, 1, 2)
x_Tiempo, y_Ir, y_Rojo = [] ,[] , []

# --------------------- Inicialización del sensor max30100 --------------------- #

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# ------------------ Función que se va a llamar periodicamente ----------------- #

def tomar_medida(i, x_Tiempo, y_Ir, y_Rojo):
   

   # ------------- lectura de las medidas actuales ------------ #

   mx30.read_sensor()
   Infrarojo = int(mx30.ir)
   Rojo = int (mx30.red)
   
   # ---- añadir la x (tiempo) y la y (medeida del sensor) ---- #
   
            # x_Tiempo.append(dt.datetime.now().strftime('%M:%S.%f'))   # Para añadir fecha a cada muestra
            # Esta hace que se retrase la adquisición de datos
   
   x_Tiempo.append(i)
   y_Ir.append(Infrarojo)
   y_Rojo.append(Rojo)
   
# ----------------------------- Programa principal ---------------------------- #

while 1:
    t_ini = time.time()             
    t_duracion_entero=0
    t_parcial = 0

    while t_duracion_entero<T_muestra:      
        
        if t_parcial == 0 or t_parcial > (T_muestra/n_muestra):
            t_parcial = 0 
            t_ini1= time.time()
            tomar_medida(i, x_Tiempo, y_Ir, y_Rojo)
            i=i+1
            x_Tiempo = x_Tiempo[-65:]
            y_Ir = y_Ir[-65:]
            y_Rojo = y_Rojo[-65:]
        t_parcial = time.time()-t_ini1
        t_duracion_entero = time.time()-t_ini

    # ------------- Configurar la gráfica ------------- #    

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
    


        


