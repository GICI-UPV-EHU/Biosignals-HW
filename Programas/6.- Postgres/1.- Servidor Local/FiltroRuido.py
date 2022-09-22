'''
Se trata de un programa que grafica las seañles recogidos por los sensores.
Se tiene que haber creado un archivo CSV de cada una de las tablas de la BBDD,
para hacer esa transformación, las instrucciones que son necesarias son:

--> sudo su postgres
--> psql
--> \c data_bio                                      (Es el nombre de la base de datos)
--> copy gsr to '/tmp/GSR.csv' with delimiter ',';   (gsr -> el nombre de la tabla)
--> copy pox to '/tmp/POX.csv' with delimiter ',';   (pox -> el nombre de la tabla)

'''



import numpy as np
from  scipy import signal
import pandas as pd
import matplotlib.pyplot as plt

def FiltroGSR(Direccion):
    Datos_or = pd.read_csv(Direccion, header= None)
    Data = Datos_or[1].to_numpy()

    print (Data)

    '''
    Ahora va el código del filtro butterworth paso bajo
    '''

    b, a = signal.butter(8, 0.05 , 'lowpass')

    Data_filtrado = signal.filtfilt(b,a, Data)
    val = Data_filtrado.size * 10/100
    print(val)

    '''
    Ahora va el código del filtro media movil
    '''
    Data_MedMov = Datos_or[1].rolling(150).mean()

    x = np.arange(0,val, 0.1)


    plt.plot(x, Data, color = [22/255, 51/255, 237/255], linewidth = 2)
    plt.plot(x, Data_filtrado, color= [237/255, 60/255, 60/255], linewidth = 2)
    plt.plot(x, Data_MedMov, color= [0/255, 198/255, 24/255], linewidth = 2)

    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('GSR signal (μS)')
    plt.grid()
    plt.title('GSR acquisition - Gain = 4.7k/0.22k+1 = 23.3636\n(2 min of relaxing video at the start of acquisition)')
    plt.legend(["Acquired GSR Signal","Filtered Acquired GSR Signal\n(Butterwoth - lowpass)", "Filtered Acquired GSR Signal\n(Moving Media - w =150)"])
    plt.show()


def FiltroPOX(Direccion):
    Datos_or = pd.read_csv(Direccion, header= None)
    DataRed = Datos_or[1].to_numpy()
    DataIR = Datos_or[2].to_numpy()


    '''
    Ahora va el código del filtro butterworth paso bajo
    '''

    b, a = signal.butter(6, 0.4 , 'lowpass')

    Data_filtradoRed = signal.filtfilt(b,a, DataRed)
    Data_filtradoIR = signal.filtfilt(b,a, DataIR)
    val = Data_filtradoRed.size * 25/1000
 
    '''
    Ahora va el código del filtro media movil
    '''
    DataRed_MedMov = Datos_or[1].rolling(5).mean()
    DataIR_MedMov  = Datos_or[2].rolling(5).mean()

    x = np.arange(0,val, 0.025)

    '''
    Figura datos POX con y sin media movil
    '''
    plt.subplot(1,2,1)
    plt.plot(x[2000:2500], DataRed[2200:2700], color = [54/255,56/255,65/255], linewidth = 2)
    #plt.plot(x[2000:2500], Data_filtradoRed[2200:2700], color= [237/255, 60/255, 60/255])
    plt.plot(x[2000:2500], DataRed_MedMov[2200:2700], color= [237/255, 60/255, 60/255])
    plt.legend(["Acquired Red POX Signal", "Filtered Acquired Red POX Signal\n(Moving Media - w = 5)"])
    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('Red Signal POX (ADC units)')
    plt.grid()
    plt.title('Acquisition of RED sensor ')

    plt.subplot(1,2,2)
    plt.plot(x[2000:2500], DataIR[2200:2700], linewidth = 2, color = [54/255,56/255,65/255])#[22/255, 51/255, 237/255])
    #plt.plot(x[2000:2500], Data_filtradoRed[2200:2700], color= [237/255, 60/255, 60/255])
    plt.plot(x[2000:2500], DataIR_MedMov[2200:2700], color= 'green', linewidth = 2)#[237/255, 60/255, 60/255])
    plt.legend(["Acquired IR POX Signal", "Filtered Acquired IR POX Signal\n(Moving Media - w = 5)"])
    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('Infrared Signal POX (ADC units)')
    plt.grid()
    plt.title('Acquisition of IR sensor ')
    
    plt.suptitle('POX acquisition\nWith Moving Media')
   
    plt.show()

    '''
    Figura datos POX con y sin filtro pasabajo butterworth
    '''
    plt.subplot(1,2,1)
    plt.plot(x[2000:2500], DataRed[2200:2700], color = [54/255,56/255,65/255], linewidth = 2)
    plt.plot(x[2000:2500], Data_filtradoRed[2200:2700], color= [237/255, 60/255, 60/255], linewidth= 2)
    plt.legend(["Acquired Red POX Signal", "Filtered Acquired Red POX Signal\n(Butterworth - Order = 6 - w = 0.4)"])
    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('Red Signal POX (ADC units)')
    plt.grid()
    plt.title('Acquisition of RED sensor ')

    plt.subplot(1,2,2)
    plt.plot(x[2000:2500], DataIR[2200:2700], linewidth = 2, color = [54/255,56/255,65/255])#[22/255, 51/255, 237/255])
    plt.plot(x[2000:2500], Data_filtradoIR[2200:2700], color= 'green', linewidth = 2)
    plt.legend(["Acquired IR POX Signal", "Filtered Acquired IR POX Signal\n(Butterworth - Order = 6 - w = 0.4)"])
    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('Infrared Signal POX (ADC units)')
    plt.grid()
    plt.title('Acquisition of IR sensor ')
    
    plt.suptitle('POX acquisition\nWith Lowpass Butterworth Filter')
   
    plt.show()


'''
Programa principal
'''

dirPOX = '/tmp/POX.csv'
FiltroPOX (dirPOX)

dirGSR = '/tmp/GSR.csv'
FiltroGSR(dirGSR)


