# mv source_file target_directory
import shutil

import psycopg2
import os

import multiprocessing as mp 
import BiblioTareasPeriodicas_ServerLocal
import time

def MoverDatos():
    shutil.move("/home/pi/Desktop/Data/esp32/POX.csv","/home/pi/Desktop/Data/BBDD/POX.csv")
    shutil.move("/home/pi/Desktop/Data/esp32/GSR.csv","/home/pi/Desktop/Data/BBDD/GSR.csv")
    conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')

    cur = conn.cursor()

    pox = open('/home/pi/Desktop/Data/BBDD/POX.csv', 'r')
    gsr = open ('/home/pi/Desktop/Data/BBDD/GSR.csv', 'r')
    cur.copy_from(pox, 'pox', sep=",")
    pox.close()
    cur.copy_from(gsr, 'gsr', sep=",")
    gsr.close()

    cur.close()
    conn.commit()
    conn.close()
    os.remove("/home/pi/Desktop/Data/BBDD/POX.csv")
    os.remove("/home/pi/Desktop/Data/BBDD/GSR.csv")

    print("La copia a la base de datos se ha completado")

t0 = time.time()
tarea1 = mp.Process(target = BiblioTareasPeriodicas_ServerLocal.Tarea_Periodica_SubidaDatos, args = (t0, 1, 60, 58, MoverDatos))

tarea1.start()
tarea1.join()

def copia_datos():
    conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')

    cur = conn.cursor()
    pox = open('/home/pi/Desktop/Data/BBDD/POX.csv', 'r')
    gsr = open ('/home/pi/Desktop/Data/BBDD/GSR.csv', 'r')
    cur.copy_from(pox, 'pox', sep=",")
    pox.close()
    cur.copy_from(gsr, 'gsr', sep=",")
    gsr.close()

    cur.close()
    conn.commit()
    conn.close()
    os.remove("/home/pi/Desktop/Data/BBDD/POX.csv")
    os.remove("/home/pi/Desktop/Data/BBDD/GSR.csv")
#copia_datos()