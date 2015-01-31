Abfahrtsgarten

Descr:
This project depends on an interactive installation of an arrival monitor at home. It is configured for local passenger transport of Dresden (only) because it just uses
the public webservice of the DVB.

Futher information and pictures of the resulted gadget at 
	http://fprager.de/tophat-2k/

Feel free to adapt the idea on your purpose. 


CONTENTS OF THIS FILE
---------------------
   
 * Introduction
  The installation uses an Raspberry PI for the higher logic and an Arduino to play the actor. So the whole project is devided in two main scripts (for each platform).
  Both boards communicate via Serial.

 * Requirements
  Raspberry Pi - Script:
	There are several nesessary configurations of the Raspberry Pi to work like an adapter to the Internet (Rasbian XY as Bootsystem, WIFI connectivity, Python 3, ...). 
	So yes, one of the most important requirement is an internet connection.  
  Arduino
	This requirements depands on the kind of output you want to use to show the bus-arrival-time. The script of this setup "presumes" an output on a 8x8 matrix and a servo-motor.
	The Arduino needs the following libraries: 
		Adafruit_LEDBackpack 	: https://github.com/adafruit/Adafruit-LED-Backpack-Library/blob/master/Adafruit_LEDBackpack.h
		Adafruit_GFX		: https://github.com/adafruit/Adafruit-GFX-Library
		Wire	
		Servo	
		
			

  additional info:
	The Arduino is connected to one USB-Port of the Raspberry Pi.
	The Servo-Motor needs an EXTRA, SEPERATED power-source. Otherwise it pulls to much power of the arduino -> raspberry pi and both boards freeze.
	You may need some buttons to make some inputs too. 

 * Recommended modules
   Raspberry Pi
	WIFI-Adapter
	Micro-USB-Powersupply
	USB-Cable to the Arduino
   
   Arduino
	8x8-LED-Matrix
	Servo-Motor with separeted power-source
	
 * Installation

   1. Befor you connect the Arduino with the Raspberry Pi, load the "actor"-script on it via a PC-Connection. 
   2. After this you can hook the output-modules on the this board. Pay attention on the PIN-Definition in the uses Script!
   3. Configure your Raspberry Pi to offer a WIFI-Access to easily use it at the buildin-state of the installation.
   4. I recommand to test the whole setup on a prototype-setup where you can rehook or exchange parts without destruction.
   5. Save the RaspberryPi-Logic (all pythons scripts) in a seperate folder on the system.
   6. Test the script with "sudo python main.py".
   7. If it works, you should first see a "hallo"-message and after some delay (requests) it shows the bus time.
   8. Configure the Pi to autostart this script by following these instructions:
	http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/auto-running-programs
   
   [9. If you wanna make it more eco-friendly, you can add a power-switch on the power-source of the raspberry pi two shut down the arrival monitor and save power.]

 * Configuration

   main.py

   actor.ino


 * Troubleshooting
 * FAQ
 * Maintainers