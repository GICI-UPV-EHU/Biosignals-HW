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
    tabla1 = tabla_or.iloc[: , 0:3]
    tabla2 = tabla_or.iloc[: , 3:6]
    tabla3 = tabla_or.iloc[: , 6:9]
    tabla4 = tabla_or.iloc[: , 9:]

    tabla1.columns = ['Time', 'Red', 'IR']
    tabla2.columns = ['Time', 'Red', 'IR']
    tabla3.columns = ['Time', 'Red', 'IR']
    tabla4.columns = ['Time', 'Red', 'IR']

    tabla_nueva = pd.concat([tabla1,tabla2,tabla3,tabla4], axis = 0,ignore_index=True)


    tabla_nueva.sort_values(by = ['Time'], inplace=True)
    tabla_nueva.reset_index(drop=True, inplace=True)
    tabla_nueva.to_csv(Direccion, header=False, index=False)
