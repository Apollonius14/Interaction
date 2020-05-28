# Interaction

There are several reasons why Matplotlib is not great for live plotting, interative programmes and games.

But... if you must, these demo files show you ways of getting python to allow Matplotlib to listen for external events and ensure the plotter reacts to them. 

In all cases, you must set up your listeners/event hooks/call backs *before* calling plt.show() -- once that happens, python struggles to execute the rest of your script, even if you use multiprocessing to run parallel processes, or multithreading.

## Contents of this repo

For all scripts: It's cleaner to have all of the initialisation function, plotter and callback function as part of the same class to keep memory references simple. 

Option 1: Use matplotlib's inbuilt event handler fig.canvas.mpl_connect. This is documented fairly well here https://matplotlib.org/3.2.1/users/event_handling.html but it is limited to certain keyboard and mouse events within the figure. Check Integrated_Event_Handler.py

Option 2: Use python's multiprocessing module to set up two parallel processes: one for the plotter and one for the source of external data or events. You can communicate between the processes using a pipe. Example shown in Parallel_Process_Writer.py

Option 3: Use matplotlib's inbuilt timer option that calls another function at specified intervals (callback) that function can be customised in the way you'd like - more flexible input options, such as a keylogger or a joystick.

Example 3A: Callback_Timer_Process.py for a general generator process
          Custom_Event_Handler.py -- keylogger although you'll need sudo permissions and the keyboard library (pip) for the last one.
          
Example 3B: Quiver_joy_callback.py -- uses the converted Analogue signal from a rapsberry pi joystick to control the orientation of a 2D matplotlib quiver plot. [ You need to run on a raspberry pi connected like example 12.1.1 here https://github.com/Freenove/Freenove_Ultrasonic_Starter_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf_]
          
          
          
