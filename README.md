<h1>Abfahrtsgarten</h1>

This project depends on an interactive installation of an arrival monitor at home. It is configured for local passenger transport of Dresden (only) because it just uses
the public webservice of the DVB.

Futher information and pictures of the resulted gadget at 
	http://fprager.de/tophat-2k/

Feel free to adapt the idea on your purpose. 


CONTENTS OF THIS FILE
---------------------
   
 <h2>Introduction</h2>

<p>The installation uses an Raspberry PI for the higher logic (the Thinker) and an Arduino to play the Actor. So the whole project is devided in two main scripts (for each platform).
Both boards communicate via Serial.</p>


  <h2>Requirements</h2>

<h3>Raspberry Pi</h3>

<p>There are several nesessary configurations of the Raspberry Pi to work like an adapter to the Internet (Rasbian XY as Bootsystem, WIFI connectivity, Python 3, ...). 
So yes, one of the most important requirement is an internet connection. </p>
  

<h3>Arduino</h3>

This requirements depands on the kind of output you want to use to show the bus-arrival-time. The script of this setup "presumes" an output on a 8x8 matrix and a servo-motor.
The Arduino needs the following libraries:
 
		CmdMessenger		: https://github.com/thijse/Arduino-Libraries/tree/master/CmdMessenger

		Adafruit_LEDBackpack 	: https://github.com/adafruit/Adafruit-LED-Backpack-Library/blob/master/Adafruit_LEDBackpack.h

		Adafruit_GFX		: https://github.com/adafruit/Adafruit-GFX-Library

		Wire	

		Servo	
		
			
<h3>additional info:</h3>

The Arduino is connected to one USB-Port of the Raspberry Pi.
The Servo-Motor needs an EXTRA, SEPERATED power-source. Otherwise it pulls to much power of the arduino -> raspberry pi and both boards freeze.
Connect a transistor between the powersource of the servo and the servo which will be controlled by the arduino. This makes it possible to switch off the
the power-consumtion of the servo while it's not moving (recommanded for battery use).
You may need some buttons to make some inputs too. 


 <h2>Recommended modules</h2>

<h3>Raspberry Pi</h3>

    * WIFI-Adapter
    * Micro-USB-Powersupply
    * USB-Cable to the Arduino
   
<h3>Arduino</h3>

    * 8x8-LED-Matrix
    * Servo-Motor with separeted power-source
    * pNp-Transistor
	
 <h2>Installation</h2>

   1. Befor you connect the Arduino with the Raspberry Pi, load the "actor"-script on it via a PC-Connection. 
   2. After this you can hook the output-modules on the this board. Pay attention on the PIN-Definition in the uses Script!
   3. Configure your Raspberry Pi to offer a WIFI-Access to easily use it at the buildin-state of the installation.
   4. I recommand to test the whole setup on a prototype-setup where you can rehook or exchange parts without destruction.
   5. Save the RaspberryPi-Logic (all pythons scripts) in a seperate folder on the system.
   6. Test the script with "sudo python main.py".
   7. If it works, you should first see a "hallo"-message and after some delay (requests) it shows the bus time.
   8. Configure the Pi to autostart this script by following these instructions:
	http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/auto-running-programs
   
   9. "optional" If you wanna make it more eco-friendly, you can add a power-switch on the power-source of the raspberry pi two shut down the arrival monitor and save power.

<h2>Configuration</h2>

<h3>Thinker</h3>

   dvb.py

    _wantedBusLines		: its an array of buslines that are of interest, 

					e.g. the bus number 85 which has the directions "Striesen" and "Btf. Gruna"

						_wantedBusLines = 	[

  									 util.make_busline(85, "Striesen", -1, True),

  									 util.make_busline(85, "Btf. Gruna",-1)

							              	];

					so you will get the shortest arrival, which can be one of both busses

    _wantedBusStop		: for which station you ask for the busses

					e.g. in Dresden "Rathausplauen"

    _lessMinutes		: maybe you want to set some time-buffer ("I need 3 min to my station, so show me 3 min less.")

    _alternativeBusStop	: it is possible that your station (_wantedBusStop) is very important and that's why a lot of busses or trams arrive or depart there
				  the dvb-webservice just offers the next 8 or 10 arrivals so it is often not possible to get the busses of interest because they needs
				  "to long" to arrive, so you would see the times in a realy short period.

			          To fix this, it is possible to set an alternative station which will come after your wantedBusStation that is less frequently 
			          used by other traffic.

				  In the dvb-script it will be first asked for the wanted busstop. If there are no relevant information in the dvb-response it, 
				  it will use the alternative stop to ask for.

	 				e.g. on "rathausplauen" arrive 3 different buslines and 2 of them more frequently than the 85, typically the highest time on  
						the monitor would be 8 or 5 minutes, which is realy short to 

					     one station after "rathausplauen" comes "kaitzerstraﬂe" wich is just "used" by the 85, for that station it is much easier to get the 
					     next bus because no other traffic "dumps" the dvb-response

    _minToAltStation	: how long needs the bus from the wanted station to the alternative station
	
   main.py

    SECONDS_TO_REQUEST	: pause between to requests of the arrival-time

    POWER_BUTTON_PIN	: Pin-number of an GPIO - Button to get some input-signals

   actor.py

    nr-ids of the command-manager

    BAUD_RATE		: the baud-rate of the serial-connection, must be the same of the Arduino script	


<h3>Actor</h3>

   actor.ino

    BAUD_RATE 		: the baud-rate of the serial-connection, must be the same of the Raspberry Pi script
	
    BUS_PIN			: analog Signal-Pin of the Servo'''
    BUS_DRIVE_DELAY 	: how long is the interruption from one servo position to the next, means it's the bus-drive-speed
    BUS_TOGGLE_PIN		: connection to the transistor to control the power-consumption of the servo
    BUS_0_POS		: what value of the analog signal is the "lowest" position of the bus/servo
    BUS_100_POS		: what value is the "highest" position of the bus/servo

    DISPLAY_BRIGHTNESS	: see Adafruit_LEDBackpack-library which values are possible
    DISPLAY_CLEAR_SPEED	: how fast the line will come from above to clear the display, in ms
    DISPLAY_TEXT_SPEED	: Time how long the text stays in one position, in ms, means its the setting of the text-scroll-speed on the 8x8-Matrix
