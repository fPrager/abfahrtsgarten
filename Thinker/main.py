#the script will automatically start at boot
#to stop this, find out the process id and kill it
#


#!/usr/bin/python

#from urllib.request import urlopen
import urllib2  #on pi: 
import time
import util
import actor
import dvb

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#-----------------------------global variables---------------------------------------#

#input
POWER_BUTTON_PIN = 23
_powerButton = None

SECONDS_TO_REQUEST = 10

_timeFromLastRequest = 0

#------------------------------helper functions---------------------------------------#



#------------------------------main functions--------------------------------------#

#initialize environment
def setup():
  #GPIO Setup
  GPIO.setup(POWER_BUTTON_PIN,GPIO.IN)
  _powerButton = GPIO.input(POWER_BUTTON_PIN)
  print('setup done')
  actor.writeText('hallo')

#the core function of the programm
def main():
  global _timeFromLastRequest
  _timeFromLastRequest = time.time()-SECONDS_TO_REQUEST
  #print('waiting '+str(SECONDS_TO_REQUEST)+" seconds")
  shouldCleanUp = False
  
  #go into an infinite loop of requests
  while True:
    time.sleep(1)
    input = GPIO.input(POWER_BUTTON_PIN)
    
    #the "power"-switch is in ON-Position
    if(True):
      if shouldCleanUp == False:
        print("............................ start working  ")
        shouldCleanUp = True
        #minibus.driveFullRound()
        #monitor.reset_time()
      #is it time to ask dvb for new information?
      if time.time()-_timeFromLastRequest > SECONDS_TO_REQUEST:
        if dvb.do_dvb_request() != 0:
          _timeFromLastRequest = time.time()
          #everthing went nice, i hope
          #do physical output
          #minibus.driveToMin(getCurrentBusMinutes())
          try:
            urllib2.urlopen("http://www.google.com").close()
          except urllib2.URLError:
            print "Not Connected"
            actor.writeText('kein wlan')
          else:
            print "Connected"
            bustime = dvb.getCurrentBusMinutes()
            if bustime < 100:
              if bustime >= 0:
                actor.writeNumber(bustime)
            else:
              actor.writeText('>100')
      #monitor.update()
    #the "power"-switch is in OFF-Position
    #if(input  == 0):
    #  if (shouldCleanUp):
    #    print("............................. stop working")
    #    cleanup()
    #    shouldCleanUp = False

#function to go back to normal
def cleanup():
  actor.writeText('tschau')
  #minibus.driveHome()
  #monitor.clear()

#------------------------------general program logic---------------------------------------#

#initilize the programm
setup()

try:
  #starting the main()-loop
  main()
except KeyboardInterrupt:
  print('close programm')
  cleanup()
  GPIO.cleanup()          # clean up GPIO

#------------------------------general program logic----------------------------------