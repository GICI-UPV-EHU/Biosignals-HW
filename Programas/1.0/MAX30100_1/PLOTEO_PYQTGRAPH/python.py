import matplotlib.pyplot as plt
import numpy as np 

x = np.linspace(0, 10, 100)
y = np.cos(x)

fig = plt.figure()
subplot1= fig.add_subplot(2,1,1)

for p in range(50):
    p=3
    updated_x=x+p
    updated_y=np.cos(x)
    subplot1.plot(updated_x,updated_y)
    plt.draw()  
    x=updated_x
    y=updated_y
    plt.pause(0.2)
    subplot1.clear()
