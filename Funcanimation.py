import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import math
import numpy as np

datum = time.time()

t_series = np.arange(0,math.pi*2.5,math.pi/24)

style.use('fivethirtyeight')


#print (signal)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# plot(t_series,signal)

def animate(i):
	newtime = time.time()
	del_t = newtime-datum
	signal = np.sin((t_series- del_t)*2)
	ax1.clear()
	ax1.plot(t_series, signal)

ani = animation.FuncAnimation(fig,animate,interval=100)
plt.show()
	
