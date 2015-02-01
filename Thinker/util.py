import re
import simplejson as json

class Busline(object):
   def __init__(self, line = None, direction = None, minutes = 0, prefered = False):
      self.line = line
      self.direction = direction
      self.minutes = minutes
      self.prefered = prefered

def make_busline(line, direction, minutes, prefered = False):
   bus = Busline(line, direction, minutes, prefered)
   return bus

def busses_from_dvb(answer):
	rec = '[\"\,0-9a-zA-Z]*'
	answer = answer.replace('\xc3\xbc','ue');
	answer = answer.replace('\xc3\xb6','oe');
	print('check: '+answer)
	matches = re.finditer(r"[\ \"\,\.0-9a-zA-Z]*", answer); 
	i = 0
	times = []
	for m in matches:
		if len(m.group(0)) > 5 :
			times.append(str(m.group(0)))
		i=i+1
	busses = []
	for t in times:
		#t = t.replace("\"","")
		infos = t.split("\",\"")		
		for i in range(0, len(infos)):
			infos[i] = infos[i].replace("\"","")
		
		if len(infos) < 3:
			return 0

		if infos[2]=="":
			infos[2]=0
		busses.append(make_busline(int(infos[0]), infos[1], int(infos[2])))
	#TODO look up all bus information, there are some doubles
	
	return busses
	#if times:
	#	print(times)
	#else:
	#	print("unknown pattern: "+answer)
	#for index in name:
	#	print(index)

def int_from_bitarray(bits):
	return 0
