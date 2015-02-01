import urllib2  #on pi: 
from urllib2 import HTTPError
import time
import util
import actor

#bus lines of interest
_wantedBusLines = [
  util.make_busline(85, "Striesen", -1, True),
  util.make_busline(85, "Btf. Gruna",-1)
];


#station info
_wantedBusStop = 'rathausplauen'
_lessMinutes = 0
_alternativeBusStop = 'rathausplauen'
_minToAltStation = 4
_selectedBusIndex = 0
_numberOfRequests = 0



#function to ask dvb-webservice for recent bus info
#returns 1: Everything went fine.
#returns 0: Somethign went wrong.
def do_dvb_request():
  global _numberOfRequests 
  global _wantedBusStop
  global _lessMinutes
  global _wantedBusLines
  _numberOfRequests = _numberOfRequests+1
    #start a request on dvb
  print('update busses')
  #dvb_answer = urlopen("http://widgets.vvo-online.de/abfahrtsmonitor/Abfahrten.do?ort=Dresden&hst="+_wantedBusStop).read()  #on pi: contents = urllib2.urlopen("...")
  try:
    dvb_answer = urllib2.urlopen("http://widgets.vvo-online.de/abfahrtsmonitor/Abfahrten.do?ort=Dresden&hst="+_wantedBusStop).read()  
  except HTTPError as e:
    print("ERROR: No Internet Connection")
    actor.writeText('ERROR CONNECTION')
    return 0
  except URLError as e:
    actor.writeText('WRONG URL')
    print("ERROR: Wrong URL sended")
    return 0

  try:
    busses = util.busses_from_dvb(str(dvb_answer))
  except Exception as e:
    print("ERROR: Parsing the html-content went wrong")
    return 0

  if busses == 0:
      print("ERROR: Something went wrong. Maybe DVB send an answer which is in a bad syntax!")
      return 0
  nothing = True
  for wantedBus in _wantedBusLines:
    hasInfo = False
    print('check busses '+str(len(busses)))
    for i in range(len(busses)-1, 0, -1):
      #print('check '+ wantedBus.direction +' with '+ busses[i].direction)
      if wantedBus.direction == busses[i].direction and wantedBus.line == busses[i].line:
        wantedBus.minutes = busses[i].minutes - _lessMinutes
        hasInfo = True
        nothing = False
    wantedBus.hasInfo = hasInfo
    if hasInfo:
      print('Updated '+str(wantedBus.line)+' ('+wantedBus.direction+') to '+str(wantedBus.minutes)+' min')
    else:
      print('No Infos about '+str(wantedBus.line)+' ('+wantedBus.direction+')')
      wantedBus.minutes = -1  
  if nothing and _wantedBusStop == 'rathausplauen':
    print('.....got no times...try ' + str(_alternativeBusStop))
    return do_alternative_dvb_request()
  return 1 

#function to ask dvb-webservice for recent bus info on the alternative bus stop
#returns 1: Everything went fine.
#returns 0: Somethign went wrong.
def do_alternative_dvb_request():
  global _numberOfRequests 
  global _alternativeBusStop
  global _minToAltStation
  global _wantedBusLines
  _numberOfRequests = _numberOfRequests+1
    #start a request on dvb
  print('update busses via alternative station')
  try:
    dvb_answer = urllib2.urlopen("http://widgets.vvo-online.de/abfahrtsmonitor/Abfahrten.do?ort=Dresden&hst="+_alternativeBusStop).read()  
  except HTTPError as e:
    print("ERROR: No Internet Connection")
    actor.writeText('ERROR CONNECTION')
    return 0
  except URLError as e:
    actor.writeText('WRONG URL')
    print("ERROR: Wrong URL sended")
    return 0

  try:
    busses = util.busses_from_dvb(str(dvb_answer))
  except Exception as e:
    print("ERROR: Parsing the html-content went wrong")
    return 0

  if busses == 0:
      print("ERROR: Something went wrong. Maybe DVB send an answer which is in a bad syntax!")
      return 0
  nothing = True
  for wantedBus in _wantedBusLines:
    hasInfo = False
    print('check busses '+str(len(busses)))
    for i in range(len(busses)-1, 0, -1):
      #print('check '+ wantedBus.direction +' with '+ busses[i].direction)
      if wantedBus.direction == busses[i].direction and wantedBus.line == busses[i].line:
        wantedBus.minutes = busses[i].minutes - _minToAltStation
        hasInfo = True
        nothing = False
    wantedBus.hasInfo = hasInfo
    if hasInfo:
      print('Updated '+str(wantedBus.line)+' ('+wantedBus.direction+') to '+str(wantedBus.minutes)+' min')
    else:
      print('No Infos about '+str(wantedBus.line)+' ('+wantedBus.direction+')')
      wantedBus.minutes = -1  
  if nothing:
    print('.....got absolute no times')
    return 0
  return 1 


#function to look up the minutes of the current selected bus
def getCurrentBusMinutes():
  time = 120
  for bus in _wantedBusLines: 
    print('has info '+ str(bus.hasInfo))
    if bus.hasInfo == True and bus.minutes < time and bus.minutes >= 0:
      if bus.hasInfo == True:
        print("use this time: "+str(bus.minutes))
        time = bus.minutes  
  return time

