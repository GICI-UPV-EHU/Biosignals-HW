'''
Programa para apagar el sensor, ya que cuando le fuerzas el cierre al programa en cuestió,
el sensor se queda encendido

'''

import max30102
import smbus
if __name__ == "__main__":
    Bus = smbus.SMBus(1)  # Se selecciona el canal 1 ya que la raspi usa este 
                      # canal para la comunicación I2C - NO USA EL 0  

    Bus.write_i2c_block_data(0x57, 0x09, [0x80])
    '''
    El primero de los argumentos es la dirección del dispositivo.
    El segundo es la dirección del registro en el que se quiere escribir
    Y el tercerp, son los valores que se quieren introducir

    Estos dos últimos datos se obtienen de la biblioteca del sensor 
    MAX 30102
    '''
    
