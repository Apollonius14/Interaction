import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import numpy as np

def provider(pipe):
	Pipe_Out,Pipe_In=pipe
	x = np.arange(0,10,0.05)
	start = time.time()	
	elapsed = 0
	while elapsed < 5:
		#print (elapsed)
		#time.sleep(0.5)
		elapsed = time.time()-start
		y = np.sin(x-(elapsed*5))
		Pipe_In.send([x,y,elapsed])
		time.sleep(0.1)
	


def plotter(pipe):
	Pipe_Out,Pipe_In=pipe
	fig, ax = plt.subplots()
	elapsed = 0
	plt.ion()
	while elapsed < 5: 
		if Pipe_Out.poll():
			#print ("Receiving Pipe")
			data = Pipe_Out.recv()
			x = data[0]
			y = data[1]
			elapsed = data[2]	
		ax.plot(x,y)
		fig.canvas.draw()
		plt.show()
		ax.clear()
	plt.close()
	print ("Plotter Closed")

def main():
	Pipe_Out,Pipe_In=mp.Pipe()
	pplot = mp.Process(target = plotter, args=((Pipe_Out,Pipe_In),))
	pprovide = mp.Process(target = provider, args=((Pipe_Out,Pipe_In),))
	print ("Started")
	pplot.start()
	pprovide.start()
	pplot.join()
	pprovide.join()
	print ("Finished")

if __name__ == "__main__":
	main()



	
	
	

