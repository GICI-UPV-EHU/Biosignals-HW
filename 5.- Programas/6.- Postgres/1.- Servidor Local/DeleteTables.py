'''
        Fecha: 19/10/2022
        User: Imanol Ayude Prieto

En este programa se hará que se elimine el contenidode las tablas dentro 
de la Base de datos en la que se está trabajando (data_bio).

El motivo de la creación es, la reducción de tiempo de este proceso. 
'''


import psycopg2
import os

if __name__ == "__main__":

    conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')
    cur = conn.cursor()

    cur.execute("DELETE FROM pox;")
    print ("Contenido de la tabla POX ha sido borrada.")

    cur.execute("DELETE FROM gsr;")
    print ("Contenido de la tabla GSR ha sido borrada.")

    cur.execute("DELETE FROM gsr_but;")
    print ("Contenido de la tabla GSR_Butterworth ha sido borrada.")

    cur.execute("DELETE FROM gsr_mmov;")
    print ("Contenido de la tabla GSR_MediaMovil ha sido borrada.")

    cur.execute("DELETE FROM ecg;")
    print ("Contenido de la tabla ECG ha sido borrada.")

    cur.close()
    conn.commit()
    conn.close()
    
    print ("Proceso de borrado completado con éxito")