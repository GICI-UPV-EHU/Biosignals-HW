from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import max30100

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Grafica en tiempo real")
p = win.addPlot(title="Grafica tiempo real")

curva = p.plot()

x_Tiempo = [] # Array's para guardar los datos
y_IR = []
i=0

mx30 = max30100.MAX30100()
mx30.enable_spo2()

def Update():
   global curva, x_Tiempo, y_IR, i
    # Actualizamos los datos
    
   mx30.read_sensor()
   Infrarojo = int(mx30.ir)
   Rojo = int (mx30.red)
   x_Tiempo.append()
   y_IR.append(Infrarojo)

   x_Tiempo = x_Tiempo[-50:]
   y_Ir = y_Ir[-50:]
   
   curva.setData(x_Tiempo,y_IR)
   QtGui.QApplication.processEvents()
   i=i+1
    
while True: Update() #Actualizamos todo lo rápido que podamos.

pg.QtGui.QApplication.exec_()
