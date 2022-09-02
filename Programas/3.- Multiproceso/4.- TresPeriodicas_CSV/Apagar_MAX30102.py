'''
Programa para apagar el sensor, ya que cuando le fuerzas el cierre al programa en cuestió,
el sensor se queda encendido

'''

import max30102

if __name__ == "__main__":
    
    sensor = max30102.MAX30102
    sensor.shutdown()
    