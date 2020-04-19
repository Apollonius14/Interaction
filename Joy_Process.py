#!/usr/bin/env python3
#############################################################################
# Filename    : Joystick.py
# Description : Read Joystick state
# Author      : www.freenove.com
# modification: 2020/03/09
########################################################################
import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Pipe
from ADCDevice import *
Z_Pin = 12      # define Z_Pin
adc = ADCDevice() # Define an ADCDevice class object

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
	GPIO.setup(Z_Pin,GPIO.IN,GPIO.PUD_UP)   # set Z_Pin to pull-up mode

def destroy():
	adc.close()
	GPIO.cleanup()

def joyin(pipe):
	working = True
	Pipe_Out,Pipe_In=pipe
	while working:
		if Pipe_Out.poll():
			working = Pipe_Out.recv()     
			val_Z = GPIO.input(Z_Pin)
			val_Y = adc.analogRead(0)
			val_X = adc.analogRead(1)
			Pipe_Out.send([val_X,val_Y,val_Z])

def printer(pipe):
	print ("Reading Process Started")	
	Pipe_Out,Pipe_In = pipe
	Pipe_In.send(True)
	position_joy = [0,0,0]
	while position_joy[2] == 1:				
		print (position_joy)		
		time.sleep(0.1)
		if Pipe_In.poll():
			recieved = Pipe_In.recv()
			position_joy[0] = received[0]
			position_joy[1] = received[1]
			position_joy[2] = received[2]
		if position_joy[2] == 0:
			Pipe_In.send(False)

def main():
	print ('Program is starting ... ') # Program entrance
	setup()
	Pipe_Out,Pipe_In = Pipe()
	Reader = Process(target=joyin, args=((Pipe_Out,Pipe_In),))
	Reader.start()		
	Writer = Process(target=printer, args=((Pipe_Out,Pipe_In),))
	Writer.start()
	Writer.join()
	Reader.join()
	destroy()


if __name__ == '__main__':
	main()
    


