
import psycopg2

conn = psycopg2.connect(dbname = "data_bio", host = 'localhost', user = 'imanol', password = '0000')

cur = conn.cursor()

pox = open('/home/pi/Desktop/Data/POX.csv', 'r')
gsr = open ('/home/pi/Desktop/Data/GSR.csv', 'r')
cur.copy_from(pox, 'pox', sep=",")
pox.close()
cur.copy_from(gsr, 'gsr', sep=",")
gsr.close()

cur.close()
conn.commit()
conn.close()