import matplotlib.pyplot as plt
import matplotlib.animation as animation
import max30100

# creación de la ventana dónde se va a crear la gráfica
fig= plt.figure()

# creación de la gráfica dentro de la figura

graf_ir = fig.add_subplot(2, 1, 1)
graf_rojo = fig.add_subplot(2, 1, 2)
x_Tiempo, y_Ir, y_Rojo = [] ,[] , []

# inicialización del sensor max30100

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# función que se va a llamar periodicamente

def animate(i, x_Tiempo, y_Ir, y_Rojo):
   
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
   
   x_Tiempo = x_Tiempo[-50:]
   y_Ir = y_Ir[-50:]
   y_Rojo = y_Rojo[-50:]
   
   # Comprobación de que se recorta el array al valor indicado
   #print(x_Tiempo)
   #print(y_Ir)
   #print(y_Rojo)
   
   # formato de la gráfica  
   graf_ir.clear()
   graf_rojo.clear()
   
   graf_ir.title.set_text('Medidas infrarojas')
   graf_rojo.title.set_text('Medidas led rojo')
   
   graf_ir.tick_params(labelrotation =45)
   graf_rojo.tick_params(labelrotation = 45)
   graf_ir.plot(x_Tiempo, y_Ir, linewidth = 2, color = 'r')
   graf_rojo.plot(x_Tiempo, y_Rojo, linewidth =2, color = 'b')
   
# función que llamará periodicamente a 'animate'

ani = animation.FuncAnimation(fig, animate, fargs=(x_Tiempo, y_Ir, y_Rojo), interval =1)
plt.show()


