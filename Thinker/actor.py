#this file contains:
# the communication with the actor (Arduino)
# via serial port
# 
# the commands are defined by the actor-script
# 		and use the CmdMessenger for Arduino (http://playground.arduino.cc/Code/CmdMessenger)

# commands sending the actor:
#		ID	:	Name			:	Parameter				:	Description
#		0	:	WriteText		:	string, (bool, int)		:	send a string to show on monitor
#																optional: flag, if text sould stay, default = false
#																		  x-offset of textposition, default = 0
#		1 	:	WriteNumber		:	int						:	Write an integer on display, if less than 40 it fits on monitor,
#																otherwise it will be scrolled
#		2 	:	DrawImage		:	int[8], (bool, bool)	:	Send eigth integers representing the ROWS from top to bottom of the 8x8-monitor
#																the actor interprets the numbers bitwise to draw the pixel (1=on, 0=off)
#																optional: flag, if clear the monitor or not, default = true
#																		  flag, if image "fade in" (true) or "flash on" (false), default = true
#		3 	: 	ClearDisplay	:	(bool)					:	clears the monitor
#																optional: flag, turn all pixels on (true) or off (false), default = false
#		4 	:	SetBusPosition	: 	int 					:	wanted percentual position (between 0-100)
#		5 	: 	GetButtonState	:							:	request a button state
#		6 	:	GetErrorMsg		:							:	request the current error messege
#
# commands recieving from actor:
#		
#		7	:	SendingButtonState	:	bool				: 	current button state
#		8 	:	SendingErrorMsg		:	string				:	current error messege


import serial
import os.path
import sys
import time

BAUD_RATE = 115200		#IMPORTANT!  to use the baudrate of the actor-script
#command ids:
WRITE_TEXT_CMD = 0
WRITE_NUM_CMD = 1
DRAW_IMAGE_CMD = 2
CLEAR_DISPLAY_CMD = 3
SET_BUS_POS_CMD = 4
GET_BUTTON_STATE_CMD = 5
GET_ERROR_MSG = 6

_actor = serial.Serial('/dev/ttyACM0', BAUD_RATE)

def writeText(text):
	sendCommand(WRITE_TEXT_CMD, text)

def writeNumber(num):
	sendCommand(WRITE_NUM_CMD, num)

def sendCommand(command, param):
	_actor.write(str(command) + "," + str(param) + ";")


#ser.write('0,test;');
#ser.write('1,24;');
#ser.write('2,3,23,25,67,34,56,45;');
#ser.write('4,10;');
#ser.write('4,90;');
#print 'send something';


