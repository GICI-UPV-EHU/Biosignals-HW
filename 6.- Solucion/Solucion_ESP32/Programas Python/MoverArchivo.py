# mv source_file target_directory
import shutil

import psycopg2
import os

import multiprocessing as mp 
import BiblioTareasPeriodicas_ServerLocal
import time
import FiltroRuido
import Separador

def MoverDatos():
    DirPOX = '/home/pi/Desktop/Data/BBDD/POX.csv'
    DirECG = '/home/pi/Desktop/Data/BBDD/ECG.csv'

    shutil.move("/home/pi/Desktop/Data/esp32/POX.csv","/home/pi/Desktop/Data/BBDD/POX.csv")
    shutil.move("/home/pi/Desktop/Data/esp32/GSR.csv","/home/pi/Desktop/Data/BBDD/GSR.csv")
    shutil.move("/home/pi/Desktop/Data/esp32/ECG.csv","/home/pi/Desktop/Data/BBDD/ECG.csv")

    Separador.DecoPOX(DirPOX)
    Separador.DecoECG(DirECG)

    FiltroRuido.FiltroGSR('/home/pi/Desktop/Data/BBDD/GSR.csv')

    conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')

    cur = conn.cursor()

    pox   = open('/home/pi/Desktop/Data/BBDD/POX.csv', 'r')
    gsr   = open('/home/pi/Desktop/Data/BBDD/GSR.csv', 'r')
    ecg   = open('/home/pi/Desktop/Data/BBDD/ECG.csv', 'r')

    gsr_b = open('/home/pi/Desktop/Data/BBDD/GSR_but.csv', 'r')
    gsr_m = open('/home/pi/Desktop/Data/BBDD/GSR_mov.csv', 'r')

    cur.copy_from(pox, 'pox', sep=",")
    pox.close()
    cur.copy_from(gsr, 'gsr', sep=",")
    gsr.close()
    cur.copy_from(ecg, 'ecg', sep=",")
    ecg.close()

    cur.copy_from(gsr_b, 'gsr_but', sep=",")
    gsr.close()
    cur.copy_from(gsr_m, 'gsr_mmov', sep=",")
    ecg.close()

    cur.close()
    conn.commit()
    conn.close()

    os.remove("/home/pi/Desktop/Data/BBDD/POX.csv")
    os.remove("/home/pi/Desktop/Data/BBDD/GSR.csv")
    os.remove("/home/pi/Desktop/Data/BBDD/ECG.csv")

    os.remove("/home/pi/Desktop/Data/BBDD/GSR_but.csv")
    os.remove("/home/pi/Desktop/Data/BBDD/GSR_mov.csv")

    print("La copia a la base de datos se ha completado")

t0 = time.time()
tarea1 = mp.Process(target = BiblioTareasPeriodicas_ServerLocal.Tarea_Periodica_SubidaDatos, args = (t0, 1, 60, 30, MoverDatos))

tarea1.start()
tarea1.join()