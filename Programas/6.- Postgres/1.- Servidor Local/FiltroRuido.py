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
import pandas as pd

def FiltroGSR(Direccion):
    Datos_or = pd.read_csv(Direccion, header= None)
    Data = Datos_or[1].to_numpy()


    '''
    Ahora va el código del filtro butterworth paso bajo
    '''

    b, a = signal.butter(8, 0.05 , 'lowpass')

    Data_filtrado = signal.filtfilt(b,a, Data)


    '''
    Ahora va el código del filtro media movil
    '''
    Data_MedMov = Datos_or[1].rolling(10).mean()
    
    tiempo = Datos_or[0].to_numpy()

    dMedMov = {'time': tiempo, 'sensor_GSR': Data_MedMov}
    dButter = {'time': tiempo, 'sensor_GSR': Data_filtrado}

    Tab_GSR_MedMov = pd.DataFrame(data=dMedMov)
    Tab_GSR_Butter = pd.DataFrame(data=dButter)

    Tab_GSR_MedMov= Tab_GSR_MedMov.dropna()

    # print (Tab_GSR_MedMov)
    # print (Tab_GSR_Butter)

    Tab_GSR_Butter.to_csv('/home/pi/Desktop/Data/BBDD/GSR_but.csv', header=False, index=False)
    Tab_GSR_MedMov.to_csv('/home/pi/Desktop/Data/BBDD/GSR_mov.csv', header=False, index=False)

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
   

 
    '''
    Ahora va el código del filtro media movil
    '''
    DataRed_MedMov = Datos_or[1].rolling(5).mean()
    DataIR_MedMov  = Datos_or[2].rolling(5).mean()

    '''
    Se toma también la columna de tiempo
    '''




'''
Programa principal
'''

# dirPOX = '/home/pi/Desktop/Data/esp32/POX.csv'
# FiltroPOX (dirPOX)

# dirGSR = '/home/pi/Desktop/Data/esp32/GSR.csv'
# FiltroGSR(dirGSR)


