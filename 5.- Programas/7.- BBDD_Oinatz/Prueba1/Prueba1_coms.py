'''
        Prueba para comprobar el correcto funcionamiento de la conexión entre el 
        dispositivo y la base de datos que se encuentra en Ubuntu.
'''



import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
import cifrado_bbdd
from datetime import datetime

def insertar_sensores_bbdd_batch_queue(): 
    print("asdasdasd")
    #x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    #
    # try:

    connection = psycopg2.connect(user="admin",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host='192.168.0.101',
                                      port="5432",
                                      database="databio",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/Desktop/CertificadoSSL/bbdd.crt')
    print("Lanzamos la query...")
    cursor = connection.cursor()
        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        #while True:
            # Sacamos cada una línea de la cola FIFO
            #linea = q.get()
            # Por cada línea, sacamos ahora los elementos individuales
            #usuario=str(linea[0])
            #rojo=str(linea[1])
            #infrarrojo=str(linea[2])
            #pulso_spo2=str(linea[3])

            #sudoracion=str(linea[4])
            #fecha=str(linea[5])
    act_time = '02-02-2022 00:00:00.000'
    red_val = 25000
    ir_val = 12000

            # Preparamos la query con la insert
    postgreSQL_insert_Query = 'INSERT INTO pox (acq_time, red_val, ir_val) VALUES (%s,%s,%s);'
            # Insert con execute_batch
    valores=[(act_time, red_val, ir_val)]
    psycopg2.extras.execute_batch(cursor, postgreSQL_insert_Query, valores)
    connection.commit()
            #x+=1

    #except (Exception, psycopg2.Error) as error:
        #print("Error obteniendo datos de la tabla de PostgreSQL", error)

if __name__ == "__main__":
    insertar_sensores_bbdd_batch_queue()