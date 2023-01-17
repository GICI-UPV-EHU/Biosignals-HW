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
 

def insertar_pox(q): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        #connection = psycopg2.connect(user="admin",
                                      #password=cifrado_bbdd.texto_descifrado,
                                      #host="192.168.0.101",
                                      #port="5432",
                                      #database="databio",
                                      #sslmode = 'require',
                                      #sslrootcert = '/home/pi/Desktop/CertificadoSSL/bbdd.crt')
        
        connection = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')
        print("Lanzamos la query...")
        cursor = connection.cursor()

        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        while True:
            # Sacamos cada una línea de la cola FIFO
            linea = []
            for i in range(200):
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
            
            #cursor.executemany("INSERT INTO pox (acq_time, red_val, ir_val) VALUES (%s,%s,%s)" , linea)
            cursor.executemany("INSERT INTO pox (tiempo, sensor_rojo, sensor_infra) VALUES (%s,%s,%s)" , linea)
            print("---------------- Tarea COMS POX -------------------")
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
            
            
def insertar_gsr(q): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        #connection = psycopg2.connect(user="admin",
                                      #password=cifrado_bbdd.texto_descifrado,
                                      #host="192.168.0.101",
                                      #port="5432",
                                      #database="databio",
                                      #sslmode = 'require',
                                      #sslrootcert = '/home/pi/Desktop/CertificadoSSL/bbdd.crt')
        
        connection = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')
        print("Lanzamos la query...")
        cursor = connection.cursor()

        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        while True:
            # Sacamos cada una línea de la cola FIFO
            linea = []
            for i in range(50):
                linea.append(q.get()) 
            
            #cursor.executemany("INSERT INTO gsr (acq_time, gsr_val) VALUES (%s,%s)" , linea)
            cursor.executemany("INSERT INTO gsr (tiempo, sensor_gsr) VALUES (%s,%s)" , linea)
            print("---------------- Tarea COMS GSR -------------------")
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

            
def insertar_ecg(q): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        #connection = psycopg2.connect(user="admin",
                                      #password=cifrado_bbdd.texto_descifrado,
                                      #host="192.168.0.101",
                                      #port="5432",
                                      #database="databio",
                                      #sslmode = 'require',
                                      #sslrootcert = '/home/pi/Desktop/CertificadoSSL/bbdd.crt')
        
        connection = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')
        print("Lanzamos la query...")
        cursor = connection.cursor()

        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        while True:
            # Sacamos cada una línea de la cola FIFO
            linea = []
            for i in range(102):
                linea.append(q.get()) 
            
            #cursor.executemany("INSERT INTO ecg (acq_time, ecg_val) VALUES (%s,%s)" , linea)
            cursor.executemany("INSERT INTO ecg (tiempo, sensor_ecg) VALUES (%s,%s)" , linea)
            print("---------------- Tarea COMS ECG -------------------")
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



