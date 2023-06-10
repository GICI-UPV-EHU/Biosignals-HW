
from cryptography.fernet import Fernet
clave = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
suite_cifrado = Fernet(clave)

def cifrado_passwd():
    
    texto_cifrado = suite_cifrado.encrypt(b"*1kRzhuYj!$")   #hay que pasarlo en bytes
    return texto_cifrado

def descifrado_passwd():

    texto_cifrado = b'gAAAAABiJ4zo9YDKl2YmvwJMqXWRTa3GQZoTRCKxnEkc3M7xNtTulKK-12qhzyp_LNzWqWHrw_BNarWBvPd4y4ySd3cgLxIdnQ=='
    texto_descifrado = (suite_cifrado.decrypt(texto_cifrado)).decode("utf-8")         # la suite nos devuelve un literal byte y necesitamos un string
    return(texto_descifrado)




clave_cif = cifrado_passwd()
print (clave_cif)
clave_dc = descifrado_passwd()
print (clave_dc)