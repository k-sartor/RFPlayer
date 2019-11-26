#!/usr/bin/env python3.5
#-*- coding: utf-8 -*-
#Only to read data from RFPlayer with python
import json
import asyncio
import serial
from urllib.request import urlopen
import datetime
from time import sleep,gmtime, strftime,localtime

s = serial.Serial('/dev/ttyUSBRFP', 115200, timeout=1)	#Edit the /dev/ttyUSB according to your configuration

def debug(flag,string):
	if flag==1:
		print (string)

def read_serial():
	text = ""
	msg = s.read().decode()
	while (msg != '\n'):
		text += msg
		msg = s.read().decode()
	debug(1,text)
	#Data See https://github.com/sasu-drooz/Domoticz-Rfplayer for mor options to decode frame
	if 'ZIA33' in text:
		text=text.replace("ZIA33", "")
		DecData = json.loads(text)
		infoType = DecData['frame']['header']['infoType']
		protocol = DecData['frame']['header']['protocol']
		frequency = DecData['frame']['header']['frequency']
		SubType = DecData['frame']['infos']['subType']
		if protocol == "2":
			id= DecData['frame']['infos']['id']
			qualifier = DecData['frame']['infos']['qualifier']
			# Domoticz.Debug("id : " + str(id) + " qualifier :" + str(qualifier))
		if protocol == "3" :
			id = DecData['frame']['infos']['id']
		##############################################################################################################
		if infoType == "2":
			if SubType == "0" and protocol == "2": # Detector/sensor visonic
				if qualifier =="8" or qualifier=="4" or qualifier=="12" or qualifier=="0":
					status=0
				if qualifier == "1" :
					status=10
				if qualifier =="7" or qualifier=="2" or qualifier=="6":
					status=20
				if qualifier == "3" :
					status=30
				Battery=99
				if qualifier == "4" or qualifier =="6" or qualifier =="12":
					Battery=10	

lineinput='ZIA++RECEIVER + *'
s.write(bytes(lineinput + '\n\r',encoding='utf8'))
lineinput='ZIA++FORMAT JSON'
s.write(bytes(lineinput + '\n\r',encoding='utf8'))
loop = asyncio.get_event_loop()
loop.add_reader(s, read_serial)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
	
