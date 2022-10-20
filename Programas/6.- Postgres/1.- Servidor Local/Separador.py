'''
Se trata de un programa que descodifica la información enviada desde el ESP32.
En cada comunicación del microprocesador, se envian 4 muestras separadas por ';'
y dentro de cada muestra, se encuentra:
    - Tiempo: instante en el que se ha tomado la muestra
    - Valor Rojo: valor que se obtiene de la refreccición del rojo en el dedo
    - Valor IR: valor infrarrojo que se obtiene
    (Separados por comas)
'''

import pandas as pd


def DecoPOX(Direccion):
    tabla_or = pd.read_csv(Direccion, header = None, sep= ';|,', engine='python')
    tabla1 = tabla_or.iloc[: ,  0:3 ]
    tabla2 = tabla_or.iloc[: ,  3:6 ]
    tabla3 = tabla_or.iloc[: ,  6:9 ]
    tabla4 = tabla_or.iloc[: ,  9:12]
    tabla5 = tabla_or.iloc[: , 12:15]

    tabla1.columns = ['Time', 'Red', 'IR']
    tabla2.columns = ['Time', 'Red', 'IR']
    tabla3.columns = ['Time', 'Red', 'IR']
    tabla4.columns = ['Time', 'Red', 'IR']
    tabla5.columns = ['Time', 'Red', 'IR']

    tabla_nueva = pd.concat([tabla1,tabla2,tabla3, tabla4, tabla5], axis = 0,ignore_index=True)


    tabla_nueva.sort_values(by = ['Time'], inplace=True)
    tabla_nueva.reset_index(drop=True, inplace=True)
    tabla_nueva.to_csv(Direccion, header=False, index=False)

def DecoECG(Direccion):
    tabla_or = pd.read_csv(Direccion, header = None, sep= ';|,', engine='python')
    tabla1 = tabla_or.iloc[: ,  0:2 ]
    tabla2 = tabla_or.iloc[: ,  2:4 ]
    tabla3 = tabla_or.iloc[: ,  4:6 ]
    tabla4 = tabla_or.iloc[: ,  6:8 ]
    tabla5 = tabla_or.iloc[: ,  8:10]

    tabla1.columns = ['Time', 'ECG']
    tabla2.columns = ['Time', 'ECG']
    tabla3.columns = ['Time', 'ECG']
    tabla4.columns = ['Time', 'ECG']
    tabla5.columns = ['Time', 'ECG']

    tabla_nueva = pd.concat([tabla1,tabla2,tabla3, tabla4, tabla5], axis = 0,ignore_index=True)


    tabla_nueva.sort_values(by = ['Time'], inplace=True)
    tabla_nueva.reset_index(drop=True, inplace=True)
    tabla_nueva.to_csv(Direccion, header=False, index=False)

# DecoECG('/home/pi/Desktop/Data/esp32/ECG.csv')
# DecoPOX('/home/pi/Desktop/Data/esp32/POX.csv')