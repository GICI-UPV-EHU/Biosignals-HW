'''
Se trata de un programa que grafica las seañles recogidos por los sensores.
Se tiene que haber creado un archivo CSV de cada una de las tablas de la BBDD,
para hacer esa transformación, las instrucciones que son necesarias son:

--> sudo su postgres
--> psql
--> \c data_bio                                      (Es el nombre de la base de datos)
--> copy gsr to '/tmp/GSR.csv' with delimiter ',';   (gsr -> el nombre de la tabla)
--> copy pox to '/tmp/POX.csv' with delimiter ',';   (pox -> el nombre de la tabla)

Para pasar los datos que han generado la figura correspondiente:
(En super usuario y estando en /tmp)

--> mv POX.csv /home/pi/Desktop o GSR

'''



from matplotlib.lines import lineStyles
import numpy as np
from  scipy import signal
import pandas as pd
import matplotlib.pyplot as plt

def FiltroGSR(Direccion):
    Datos_or = pd.read_csv(Direccion, header= None)
    Data = Datos_or[1].to_numpy()


    '''
    Ahora va el código del filtro butterworth paso bajo
    '''

    b, a = signal.butter(8, 0.05 , 'lowpass')

    Data_filtrado = signal.filtfilt(b,a, Data)
    val = Data_filtrado.size * 50/100
    len = Data_filtrado.size


    '''
    Ahora va el código del filtro media movil
    '''
    Data_MedMov = Datos_or[1].rolling(10).mean()

    x = np.arange(0,val, 0.5)


    plt.plot(x[  :     ], Data                 , color = [ 22/255,  51/255, 237/255], linewidth = 1, linestyle = '-')
    plt.plot(x[  :     ], Data_filtrado        , color = [237/255,  60/255,  60/255], linewidth = 2, linestyle = '-')
    plt.plot(x[0:len-5], Data_MedMov[5:len+1], color = [ 18/255, 198/255,   0/255], linewidth = 3, linestyle = '-')

    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('GSR signal (μS)')
    plt.grid()
    plt.title('GSR acquisition - Gain = 68k1/2k2+1 = 31.9545\n(2 min of relaxing video at the start of acquisition)')
    plt.legend(["Acquired GSR Signal","Filtered Acquired GSR Signal\n(Butterwoth - lowpass)", "Filtered Acquired GSR Signal\n(Moving Media - w = 10')"])
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
    # plt.subplot(1,2,1)
    # plt.plot(x[100:250], DataRed[100:250], color = [54/255,56/255,65/255], linewidth = 2)
    # #plt.plot(x[2000:2500], Data_filtradoRed[2200:2700], color= [237/255, 60/255, 60/255])
    # plt.plot(x[100:250], DataRed_MedMov[100:250], color= [237/255, 60/255, 60/255])
    # plt.legend(["Acquired Red POX Signal", "Filtered Acquired Red POX Signal\n(Moving Media - w = 5)"])
    # plt.xlabel('time (s)', loc = 'center')
    # plt.ylabel('Red Signal POX (ADC units)')
    # plt.grid()
    # plt.title('Acquisition of RED sensor ')

    # plt.subplot(1,2,2)
    # plt.plot(x[100:250], DataIR[100:250], linewidth = 2, color = [54/255,56/255,65/255])#[22/255, 51/255, 237/255])
    # #plt.plot(x[2000:2500], Data_filtradoRed[2200:2700], color= [237/255, 60/255, 60/255])
    # plt.plot(x[100:250], DataIR_MedMov[100:250], color= 'green', linewidth = 2)#[237/255, 60/255, 60/255])
    # plt.legend(["Acquired IR POX Signal", "Filtered Acquired IR POX Signal\n(Moving Media - w = 5)"])
    # plt.xlabel('time (s)', loc = 'center')
    # plt.ylabel('Infrared Signal POX (ADC units)')
    # plt.grid()
    # plt.title('Acquisition of IR sensor ')
    
    # plt.suptitle('POX acquisition\nWith Moving Media')
   
    # plt.show()

    # '''
    # Figura datos POX con y sin filtro pasabajo butterworth
    # '''
    # plt.subplot(1,2,1)
    # plt.plot(x[200:300], DataRed[200:300], color = [54/255,56/255,65/255], linewidth = 2)
    # plt.plot(x[200:300], Data_filtradoRed[200:300], color= [237/255, 60/255, 60/255], linewidth= 2)
    # plt.legend(["Acquired Red POX Signal", "Filtered Acquired Red POX Signal\n(Butterworth - Order = 6 - w = 0.4)"])
    # plt.xlabel('time (s)', loc = 'center')
    # plt.ylabel('Red Signal POX (ADC units)')
    # plt.grid()
    # plt.title('Acquisition of RED sensor ')

    # plt.subplot(1,2,2)
    # plt.plot(x[200:300], DataIR[200:300], linewidth = 2, color = [54/255,56/255,65/255])#[22/255, 51/255, 237/255])
    # plt.plot(x[200:300], Data_filtradoIR[200:300], color= 'green', linewidth = 2)
    # plt.legend(["Acquired IR POX Signal", "Filtered Acquired IR POX Signal\n(Butterworth - Order = 6 - w = 0.4)"])
    # plt.xlabel('time (s)', loc = 'center')
    # plt.ylabel('Infrared Signal POX (ADC units)')
    # plt.grid()
    # plt.title('Acquisition of IR sensor ')
    
    # plt.suptitle('POX acquisition\nWith Lowpass Butterworth Filter')
   
    # plt.show()

    '''
    Figura datos POX sinf filtros
    '''
    plt.subplot(1,2,1)
    plt.plot(x[24500:24600], DataRed[24500:24600], color = 'red')#[54/255,56/255,65/255], linewidth = 2)
    plt.legend(["Acquired Red POX Signal"])
    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('Red Signal POX (ADC units)')
    plt.grid()
    plt.title('Acquisition of RED sensor ')

    plt.subplot(1,2,2)
    plt.plot(x[24500:24600], DataIR[24500:24600], linewidth = 2, color = 'blue')#[54/255,56/255,65/255])#[22/255, 51/255, 237/255])
    plt.legend(["Acquired IR POX Signal"])
    plt.xlabel('time (s)', loc = 'center')
    plt.ylabel('Infrared Signal POX (ADC units)')
    plt.grid()
    plt.title('Acquisition of IR sensor ')
    
    plt.suptitle('POX acquisition')
   
    plt.show()


'''
Programa principal
'''

# dirPOX = '/tmp/POX.csv'
# FiltroPOX (dirPOX)

dirGSR = '/tmp/GSR.csv'
FiltroGSR(dirGSR)



