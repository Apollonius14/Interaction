"""
Creating a matplotlib plotter object that has the ability
to listen to an external process and dynamically update.

Using the inbuilt canvas timer of matplotlibs figure which
allows matplotlib to access callbacks at set intervals. These
callbacks could be any form of event. (as opposed to mpl_connect
which only has a few inbuild types of events).

"""


import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import numpy as np
import math


class SensorPlotter:

    def __init__(self):
        self.t = []
        self.x = []
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0,20)
        self.ax.set_ylim(-2,2)

    def terminate(self):
        plt.close('all')

    def get_update(self):
        while self.pipe_end.poll():
            data = self.pipe_end.recv()
            if data is None:
                self.terminate()
                return False
            else:
                self.t.append(data[0])
                self.x.append(data[1])
                self.ax.plot(self.t,self.x,'b-')
                self.fig.canvas.draw()
            return True
            

    # the python __call__ method is inbuilt to classes
    # and allows them to be called as functions, in
    # which case they execute the below code using their
    # local variabls and others passed to them via
    # events, callbacks, pipes or queues
    
    def __call__(self,pipe):

        # This class listens in to a pipe at intervals
        # specified by a timer
        print('starting plotter...')
        self.pipe_end = pipe
        timer = self.fig.canvas.new_timer(interval=100)
        timer.add_callback(self.get_update)
        timer.start()
        plt.show()


def writer(pipe):

    writer_pipe = pipe
    elapsed = 0
    start = time.time()
    while elapsed <20:
        elapsed = time.time()-start
        t = elapsed
        x = math.sin(t)
        pipe.send([t,x])
        time.sleep(0.25)
    print ("Writer Elapsed %.2f" %elapsed)
    pipe.send(None)
    


def main():

    pipe_in, pipe_out = mp.Pipe()
    plotter = SensorPlotter()
    programme_start = time.time()
    write_process = mp.Process(target=writer,args=(pipe_in,))
    plot_process = mp.Process(target=plotter,args=(pipe_out,))

    write_process.start()
    plot_process.start()
    write_process.join()
    plot_process.join()
    programme_end = time.time()
    actual_elapsed = programme_end-programme_start
    print ("Actual Elapsed %.2f" %actual_elapsed)

if __name__ == '__main__':
    main()
    


        
