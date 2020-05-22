"""
Creating a matplotlib plotter object that has the ability
to listen to an external process and dynamically update.

Using the inbuilt canvas timer of matplotlibs figure which
allows matplotlib to access callbacks at set intervals. These
callbacks could be any form of event. (as opposed to mpl_connect
which only has a few inbuild types of events).

"""
import RPi.GPIO as GPIO
from ADCDevice import *
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import numpy as np
import math
adc = ADCDevice()
Z_Pin = 12

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
             "Please use command 'i2cdetect -y 1' to check the I2C address! \n" "Program Exit. \n");
        exit(-1)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Z_Pin,GPIO.IN,GPIO.PUD_UP)

class SensorPlotter:

    def __init__(self):
        # Meshplot parameters
        self.X = np.arange(-10, 10, 1)
        self.Y = np.arange(-10, 10, 1)
        self.xq = 0
        self.yq = 0
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)

    def terminate(self):
        plt.close()

    def get_update(self):

        self.xq += (adc.analogRead(0)-129)/64
        self.yq += (adc.analogRead(1)-126)/64
        if GPIO.input(Z_Pin) == 1:
            #print ("Joystick operating")
            self.ax.clear()
            self.U, self.V = np.meshgrid(self.X+self.xq,self.Y+self.yq)
            self.ax.quiver(self.X,self.Y,self.U,self.V)
            self.fig.canvas.draw()
        if GPIO.input(Z_Pin) == 0:
            print ("Terminating")
            self.terminate()
        return True
            

    # the python __call__ method is inbuilt to classes
    # and allows them to be called as functions, in
    # which case they execute the below code using their
    # local variabls and others passed to them via
    # events, callbacks, pipes or queues
    
    def __call__(self):

        # This class listens in to a pipe at intervals
        # specified by a timer
        print('starting plotter...')
        #self.pipe_end = pipe
        timer = self.fig.canvas.new_timer(interval=10)
        timer.add_callback(self.get_update)
        timer.start()
        plt.show()



def destroy():
    adc.close()
    GPIO.cleanup()

def main():

    setup()
    #pipe_in, pipe_out = mp.Pipe()
    plotter = SensorPlotter()
    programme_start = time.time()
    #write_process = mp.Process(target=writer,args=(pipe_in,))
    plotter()
    programme_end = time.time()
    actual_elapsed = programme_end-programme_start
    print ("Actual Elapsed %.2f" %actual_elapsed)
    destroy()

if __name__ == '__main__':
    main()
    


        
