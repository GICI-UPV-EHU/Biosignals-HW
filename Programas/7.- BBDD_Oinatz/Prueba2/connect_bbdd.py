from mmap import PAGESIZE
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
import ssl
import cifrado_bbdd
from io import StringIO
import os
import sys
import pandas as pd
from multiprocessing import Process, Queue
 

def insertar_sensores_bbdd_batch_queue(q): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        connection = psycopg2.connect(user="admin",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="192.168.0.101",
                                      port="5432",
                                      database="databio",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/Desktop/CertificadoSSL/bbdd.crt')
        print("Lanzamos la query...")
        cursor = connection.cursor()

        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        while True:
            # Sacamos cada una línea de la cola FIFO
            linea = []
            for i in range(100):
                linea.append(q.get()) 
            
            # Por cada línea, sacamos ahora los elementos individuales
            # rojo=str(linea[0])
            # infrarrojo=str(linea[1])
            # fecha=str(linea[2])
            # print(fecha)
            # Preparamos la query con la insert
            # postgreSQL_insert_Query = "INSERT INTO pox (acq_time, red_val, ir_val) VALUES (%s,%s,%s);"
            # # Insert con execute_batch
            # valores=[(fecha, rojo, infrarrojo)]
            # extras.execute_batch(cursor, postgreSQL_insert_Query, valores, page_size = 100)

            cursor.executemany("INSERT INTO pox (acq_time, red_val, ir_val) VALUES (%s,%s,%s)" , linea)
            print("---------------- Tarea COMS  -------------------")
            print("se han subido datos")
            connection.commit()

                
            if linea is None:
                break
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")
            
            


            



