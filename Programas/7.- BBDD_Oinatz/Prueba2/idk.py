import psycopg2
import cifrado_bbdd


connection = psycopg2.connect(user="admin",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="192.168.0.101",
                                      port="5432",
                                      database="databio",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/Desktop/CertificadoSSL/bbdd.crt')
print("Lanzamos la query...")
cursor = connection.cursor()