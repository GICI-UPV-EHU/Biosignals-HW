import matplotlib.pyplot as plt
import time
import numpy as np
from scipy import signal
import pandas as pd

# Datos_or = pd.read_csv('/home/pi/GITHUB/Biosignals-HW/Programas/Solucion_Raspberry/1.-Solucion_Imanol/POX/POX_1Hz.csv', header= None)
# Datos_or = pd.read_csv('/home/pi/GITHUB/Biosignals-HW/Programas/Solucion_Raspberry/1.-Solucion_Imanol/POX/POX_10Hz.csv', header= None)
Datos_or = pd.read_csv('/home/pi/GITHUB/Biosignals-HW/Programas/Solucion_Raspberry/1.-Solucion_Imanol/POX/POX_50Hz.csv', header= None)

DataRed = Datos_or[1].to_numpy()
DataIR  = Datos_or[2].to_numpy()

Len = DataIR.size*1
# x = np.arange(0,55, 1)*1
# x = np.arange(0,505, 1)*0.1
x = np.arange(0,2998, 1)*0.02


# función que se va a llamar periodicamente
plt.subplot(2,1,1)
# plt.plot(x[25:55], DataRed[25:55], color = 'red')#[54/255,56/255,65/255], linewidth = 2)
# plt.plot(x[100:400], DataRed[100:400], color = 'red')#[54/255,56/255,65/255], linewidth = 2)
plt.plot(x[1000:2500], DataRed[1000:2500], color = 'red')#[54/255,56/255,65/255], linewidth = 2)

plt.legend(["Acquired Red POX Signal"])
plt.xlabel('time (s)', loc = 'center')
plt.ylabel('Red Signal POX (ADC units)')
plt.grid()
plt.title('Acquisition of RED sensor ')

plt.subplot(2,1,2)
# plt.plot(x[25:55], DataIR[25:55], linewidth = 2, color = 'blue')#[54/255,56/255,65/255])#[22/255, 51/255, 237/255])
# plt.plot(x[100:400], DataIR[100:400], linewidth = 2, color = 'blue')#[54/255,56/255,65/255])#[22/255, 51/255, 237/255])
plt.plot(x[1000:2500], DataIR[1000:2500], linewidth = 2, color = 'blue')#[54/255,56/255,65/255])#[22/255, 51/255, 237/255])

plt.legend(["Acquired IR POX Signal"])
plt.xlabel('time (s)', loc = 'center')
plt.ylabel('Infrared Signal POX (ADC units)')
plt.grid()
plt.title('Acquisition of IR sensor ')
    
# plt.suptitle('POX acquisition (1 HZ)')
# plt.suptitle('POX acquisition (10 HZ)')
plt.suptitle('POX acquisition (50 HZ)')
plt.show()
