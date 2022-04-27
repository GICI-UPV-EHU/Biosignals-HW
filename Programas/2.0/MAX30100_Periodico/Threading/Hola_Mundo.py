from concurrent.futures import thread
import threading
import time
def print_hello_three_times():
    while 1:
        time.sleep(0.05)
        print(t_0-time.time())
        
def print_hi_three_times():
    
    while 1:    
        t_1=time.time()
        print('asd')
        t_2=time.time()-t_1
        time.sleep(0.1-t_2)

Tarea1= threading.Thread(target=print_hello_three_times)
Tarea2= threading.Thread(target=print_hi_three_times)


t_0=time.time()
Tarea1.start()
Tarea2.start()