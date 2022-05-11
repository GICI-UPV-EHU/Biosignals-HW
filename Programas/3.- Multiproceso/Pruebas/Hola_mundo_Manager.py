import multiprocessing as mtp
import time

def hacer (LIST):
    nextcall=time.time()

    for i in range(10):
        LIST.append(i)
        print("a")
        nextcall = nextcall + 0.05
        time.sleep(nextcall - time.time())
        
def hacer2 (LIST1):
    nextcall=time.time()
    
    for i in range(20):
        
        LIST1.append(i)
        print("b")
        nextcall = nextcall + 0.025
        time.sleep(nextcall - time.time())


mng = mtp.Manager()
L = mng.list()

p = mtp.Process(target= hacer, args=(L,))
p2 = mtp.Process(target = hacer2, args=(L,))
p.start()
p2.start()
p.join()
p2.join()
print(L)
L.clear()
print(L)

        

