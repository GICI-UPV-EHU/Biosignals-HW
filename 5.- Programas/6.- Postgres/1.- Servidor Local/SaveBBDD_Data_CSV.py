'''
        Fecha: 19/10/2022
        User: Imanol Ayude Prieto

En este programa se hará que coja los datos de cada una de las tablas
de la base de datos, y los guarde en un CSV, para así poder comporbar
el periodo de cada una de las adquisiciones de señales.

A dia de hoy, los periodos debería de ser_

    -> POX: 100 ms --  10 Hz
    -> GSR:   1  s --   1 Hz
    -> ECG:  10 ms -- 100 Hz

'''


import psycopg2
import shutil

if __name__ == "__main__":

    conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')
    cur = conn.cursor()

    cur.execute("copy pox to '/tmp/POX.csv' with delimiter ','")
    print ("Contenido de la tabla POX ha sido copiado.")

    cur.execute("copy gsr to '/tmp/GSR.csv' with delimiter ','")
    print ("Contenido de la tabla GSR ha sido copiado.")

    cur.execute("copy ecg to '/tmp/ECG.csv' with delimiter ','")
    print ("Contenido de la tabla GSR_Butterworth ha sido copiado.")



    cur.close()
    conn.commit()
    conn.close()
    


    print ("Proceso de borrado completado 9con éxito")