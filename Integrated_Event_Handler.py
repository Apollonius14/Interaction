
# Import Packages
#--------------------------------------------------------------------------------------------------#
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import numpy as np
import math
import time
import threading

# Define Functions
#--------------------------------------------------------------------------------------------------#

# A routine to get a lung volume time series profile assuming exponential inhale and exhale for now
# Arguments P_Vol for peak tidal volume in cm3
# Ratio: the ratio of the exhalation phase to inhalation
# bpm: breaths per minute
# Returns two numpy arrays t series and Volume series of same size
# Also returns duration which is a float equal to 60/bpm

def get_optimal(P_Vol,ratio,bpm):

	Duration = math.floor(60/bpm)
	# Can Create this from number of breaths per minute
	t = np.arange(0,Duration,Duration/100)
	
	# Pick Index for Peak
	P_index = math.floor(len(t)/(1+ratio))

	# Inhalation curve
	Vol = np.zeros(t.shape)

	# Scale inhalation curve to taper to 2% gradient ahead of peak
	a = 3
	
	#Create inhalation curve
	for i in range(len(Vol)):
		Vol[i] = P_Vol*(1-math.exp(-t[i]*a))

	# Exhalation Curve
	#--- Ensure joining at peak (solve for b)
	#--- Ensure near zero at end (solve for c)

	b = np.log(P_Vol)+t[P_index]

	for i in range(P_index+1,len(Vol),1):
		Vol[i] = (math.exp(-1*t[i]+b))
	

	return t,Vol,Duration


# Plot initialisation function
# Creating two empty series
# Line1 is the optimal breathing profile (static, set once by user)
# Line2 is dynamic breathing profile (coming from generator at the moment, could come from input)

def init():
	line1.set_data([],[])
	line2.set_data(t,Vol)
	return line1,line2

# Animation loop

def animate(i,t,Vol,Duration,start):			
	newtime = time.time()
	elapsed = newtime-start	
	proportion = (elapsed/Duration)
	global signal

	# The number of the cycle	
	cycle = int(elapsed/Duration)
	
	# The proportion of the curreny cycle completed
	proportion = proportion - cycle	
	
	if cycle == 0:
		
		signal = np.zeros(t.shape)

		for i in range(math.floor(len(Vol)*proportion)):
		
			signal[i] = Vol[i]*scale

	if cycle > 0:
		
		
		index = math.floor(len(Vol)*proportion)

		signal[index-1] = Vol[index-1]*scale

		

	line1.set_data(t,signal)

	return line2,line1

# Key Acquistion Function 

def onbutt(event):	
	global scale
	if event.key=='down':
		scale*=1.05
	if event.key=='up':
		scale*=0.95
	if event.key=='q':
		plt.close(fig)
		scale = -1



# Plotter Function 

def plotter():
	global fig
	fig = plt.figure()
	global line1
	global line2	
	ax1 = plt.axes(xlim=(0,Duration),ylim=(0,P_Vol+2))				
	ax1.autoscale(False)
	line1,=ax1.plot([],[],'r-',lw=1)
	line2,=ax1.plot([],[],lw=3)
	# Make a Short Plot Tracker in Red that simulates breathing
	start = time.time()

	fig.canvas.mpl_connect('key_press_event',onbutt)

	ani = animation.FuncAnimation(fig,animate,fargs=(t,Vol,Duration,start),init_func=init,
	              interval=(bpm/60),repeat=True,blit=True)
	plt.show()

def gimmick():
	for i in range(10):
		print (i)
		time.sleep(1)


# Main Script

#--------------------------------------------------------------------------------------------------#


### (1) Set Ideal Breathing Profile

# Get Ideal Breathing Profile
ratio = 1.5
#ratio = float(input("Enter Exhale-Inhale Ratio between 1.25 and 2.5"))
P_Vol = 40
#P_Vol = float(input("Enter Peak tidal Volume cm3"))
bpm =10
#bpm = float(input("Enter breaths per minute between 10 and 25"))
(t,Vol,Duration) = get_optimal(P_Vol, ratio, bpm)

### (2) Set Up Animation thread
print ("Welcome to the breathing plotter")
print ("________________________________")
print ("Move your cursor into the chart ")
print ("area and then use the up arrow  ")
print ("to simulate deeper breaths, down")
print ("to simulate shallower breaths.  ")
print ("________________________________")
print ("press q to quit                 ")
#gimmi = threading.Thread(target=gimmick)
#gimmi.start()
scale=1
plotter()





