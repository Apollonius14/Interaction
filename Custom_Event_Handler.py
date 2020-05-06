"""
Creating a matplotlib plotter object that has the ability
to listen to an external process and dynamically update.

Using the inbuilt canvas timer of matplotlibs figure which
allows matplotlib to access callbacks at set intervals. These
callbacks could be any form of event. (as opposed to mpl_connect
which only has a few inbuild types of events).

"""

import keyboard as kb
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import numpy as np
import math
import keyboard as kb

class SensorPlotter:

    def __init__(self):
        self.X = np.arange(-5, 5, 1)
        self.Y = np.arange(-5, 5, 1)
        self.x = 0
        self.y = 0
        self.start = time.time()
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-5,5)
        self.ax.set_ylim(-5,5)

    def terminate(self):
        plt.close('all')

    def get_update(self):
        elapsed = time.time() - self.start
        if elapsed < 10:
            kb.start_recording()
            time.sleep(0.08)
            events= kb.stop_recording()
            if len(events)>1:
                if events[0].name == "up":
                    self.y += 1
                if events[0].name == "down":
                    self.y += -1
                if events[0].name == "right":
                    self.x += 1
                if events[0].name == "left":
                    self.x -= 1
                    
            self.ax.clear()
            self.U, self.V = np.meshgrid(self.X+self.x,self.Y+self.y)
            self.ax.quiver(self.X,self.Y,self.U,self.V)
            self.fig.canvas.draw()
        else:
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
        timer = self.fig.canvas.new_timer(interval=90)
        timer.add_callback(self.get_update)
        timer.start()
        plt.show()


def main():

    plotter = SensorPlotter()
    programme_start = time.time()
    plotter()
    programme_end = time.time()
    actual_elapsed = programme_end-programme_start
    print ("Actual Elapsed %.2f" %actual_elapsed)

if __name__ == '__main__':
    main()
    


        
