"""
Creating a matplotlib plotter object that has the ability
to listen to an external process and dynamically update.

Using the inbuilt canvas timer of matplotlibs figure which
allows matplotlib to access callbacks at set intervals. These
callbacks could be any form of event. (as opposed to mpl_connect
which only has a few inbuild types of events).

"""

import time
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
from mgen import rotation_from_angles as rotate


class DronePlotter:

    def __init__(self):

        # End points of drone - a simple cross with a hat
        # Points stored in self.body 6 X 3 matrix with each row being of form [x,y,z] coordinate
        self.body = np.array([[0,0,0],[0,0,2],[-2,0,0],[2,0,0],[0,-2,0],[0,2,0]])
        self.base = self.body[0,:]
        self.head = self.body[1,:]
        self.wing1R = self.body[2,:]
        self.wing1L = self.body[3,:]
        self.wing2R = self.body[4,:]
        self.wing2L = self.body[5,:]
        self.started = False

        # Initialise simulation time and scene
        self.start = time.time()
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.ax.set_xlim(-10,10,auto = False)
        self.ax.set_ylim(-10,10, auto = False)
        self.ax.set_zlim(-10,10, auto = False)

        #Initialise Empty Model
        self.headP =  self.ax.plot([],[],[])
        self.wing1P = self.ax.plot([],[],[])
        self.wing2P = self.ax.plot([],[],[])


    def terminate(self):
        plt.close('all')

    def get_update(self):
        elapsed = time.time()-self.start
        if elapsed > 20:
            self.terminate()
        else:
            # To do -- use more compressed numpy array transformations
            start = time.time()
            # Displacement
            displacement = np.array([math.sin(2*elapsed),math.cos(2*elapsed),0])
            self.body = self.body + np.array([displacement,displacement,displacement,displacement,displacement,displacement])

            # 3D Rotation
            rotation = rotate([elapsed/2,elapsed/5,0],'XYZ')

            
            self.base = rotation.dot(self.body[0,:])
            self.head = rotation.dot(self.body[1,:])
            self.wing1R = rotation.dot(self.body[2,:])
            self.wing1L = rotation.dot(self.body[3,:])
            self.wing2R = rotation.dot(self.body[4,:])
            self.wing2L = rotation.dot(self.body[5,:])
            end = time.time()
            drawingtime = end-start
            print(drawingtime)
            

            self.ax.clear()
            
            #self.t = elapsed
            start = time.time()
            self.headP =  self.ax.plot([self.base[0],self.head[0]],[self.base[1],self.head[1]],[self.base[2],self.head[2]],"b-")
            self.wing1P = self.ax.plot([self.wing1L[0],self.wing1R[0]],[self.wing1L[1],self.wing1R[1]],[self.wing1L[2],self.wing1R[2]])
            self.wing2P = self.ax.plot([self.wing2L[0],self.wing2R[0]],[self.wing2L[1],self.wing2R[1]],[self.wing2L[2],self.wing2R[2]])
            self.ax.set_xlim(-10,10,auto = False)
            self.ax.set_ylim(-10,10, auto = False)
            self.ax.set_zlim(-10,10, auto = False)
            
            #line = self.ax.plot(self.t,self.x,self.y,'b-')
            self.fig.canvas.draw()
        return True
            

    # the python __call__ method is inbuilt to classes
    # and allows them to be called as functions, in
    # which case they execute the below code using their
    # local variabls and others passed to them via
    # events, callbacks, pipes or queues
    
    def __call__(self):

        print('starting plotter...')
        timer = self.fig.canvas.new_timer(interval=15)
        timer.add_callback(self.get_update)
        timer.start()
        plt.show()


def main():

    plotter = DronePlotter()
    programme_start = time.time()
    plotter()
    programme_end = time.time()
    actual_elapsed = programme_end-programme_start
    print ("Actual Elapsed %.2f" %actual_elapsed)

if __name__ == '__main__':
    main()
    


        
