#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

import serial
import io
import time
import datetime
import requests
import os.path
import traceback
import sys
from standards import *

baud                = 9600   # baud rate for serial port
verbose             = False
req_timeout         = 5

for arg in sys.argv:
	if arg == '-e':
		emoncms_update = True
		print("EMONCMS Updating is ON")
	elif arg == '-l':
		txt_logging = True
		print("Logging to file is ON")
	elif arg == '-t':
		thingspeak_update = True
		print("THINGSPEAK Updating is ON")
	elif arg == '-v':
		verbose = True
		print("VERBOSE is ON")
	elif arg == '-vv':
		verbose_verbose = True
		print("VVVVVERBOSE is ON")
	elif arg == '-h':
		print("Gateway_Logger.py script - LWH & NHH")
		print("Backend processing of data collected by Arduino based sensors for output to SVG/PNG file")
		print("Options:  [-e EMONCMS UPDATING ON (default)] [-l LOGGING TO FILE (default)]")
		print("[-t THINGSPEAK UPDATING ON (default)] [-v VERBOSE] [-h HELP]")
		sys.exit()

def serial_data(port, baudrate):
	while True:
		try:
			pt = serial.Serial(port, baudrate, timeout=600)
			spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1), errors='strict',line_buffering=True)
			while True:
				buffer = spb.readline()
				if buffer:
					yield buffer
					if verbose:
						print("YIELDING DATA")
				else:
					if verbose:
						print("ELSE, BREAKING")
					break
			pt.close()
		except Exception:
			print("ERROR: SERIAL_DATA")
			traceback.print_exc(file=sys.stdout)

for buffer in serial_data(gateway_addr, 9600):
	try:
		now = time.strftime("%H:%M:%S")
		today = datetime.date.today()
		buffer = buffer.strip('\n')
		addr = buffer.split(',')[0]
		temp = buffer.split(',')[1].strip('T')
		press = buffer.split(',')[2].strip('P')
		humid = buffer.split(',')[3].strip('H')
		volt = buffer.split(',')[4].strip('V')
		rssi = buffer.split(',')[5]
		dew = float(temp) - (0.36 * (100 - float(humid)))
		x = str(today) + ',' + str(now) + ',' + str(buffer) + '\n'
		if verbose:
			print(x)
		if not os.path.exists('data_log'):
			os.makedirs('data_log')
		fname = str(today) + '.log'  # log file to save data in
		fdirectory = '/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m")
		fmode = 'a'  # log file mode = append
		if not os.path.exists(fdirectory):
			os.makedirs(fdirectory)
		outf = open(os.path.join(fdirectory, fname), fmode)
		outf.write(x)
		outf.flush()
	except Exception:
		print("ERROR: DATA PROCESSING", today, now, "STRING:", buffer, ":END")
		traceback.print_exc(file=sys.stdout)
	try:
		url = 'https://emoncms.org/input/post.json?node=%s&json={T:%s,P:%s,H:%s,V:%s,R:%s,D:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, temp, press, humid, volt, rssi, dew)
		r = requests.post(url, timeout=req_timeout)
		if verbose:
			if "ok" in r:
				print("EMONCMS Update OK")
			else:
				print("EMCONMS Update FAILED")
	except requests.exceptions.Timeout:
		print("ERROR: REQUESTS TIMEOUT", today, now, buffer)
	except requests.exceptions.RequestException:
		print("ERROR: EMONCMS REQUESTS", today, now, buffer)
	except Exception:
		print("ERROR: EMONCMS OTHER", today, now, buffer)
		traceback.print_exc(file=sys.stdout)
