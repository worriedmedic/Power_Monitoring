#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

import serial, io
import time
import datetime
import requests
import os.path
import traceback
import sys

addr                = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A800HQ6P-if00-port0'  # serial port to read data from
baud                = 115200   # baud rate for serial port
thingspeak_update   = True # Turn on/off updating to ThingSpeak
emoncms_update      = True # Turn on/off updating to Emoncms
verbose             = False
req_timeout         = 5

for arg in sys.argv:
	if arg == '-e':
		emoncms_update = True
		print("EMONCMS Updating is ON")
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

for buffer in serial_data(addr, baud):
	now = time.strftime("%H:%M:%S") # Call time of serial read
	today = datetime.date.today() # Call date of serial read
	addr = '10'
	try:
		buffer = buffer.strip('\n')
		ct1p = buffer.split(',')[0][4:]
		ct2p = buffer.split(',')[1][4:]
		ct3p = buffer.split(',')[2][4:]
		ct4p = buffer.split(',')[3][4:]
		volt = buffer.split(',')[4][5:]
		if verbose:
			print(ct1p,ct2p,ct3p,ct4p,volt)
		volt = float(volt) / 100
		cttotal = int(ct1p) + int(ct2p)
		if verbose:
			print(volt,cttotal)
		data_valid = True
	except Exception:
		data_valid = False
		print("DATA SPLIT ERROR", today, now, buffer)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)        
	if data_valid:
		try:
			x = str(today) + ',' + str(now) + ',' + str(buffer) + '\n'
			if verbose:
				print(x)
			if not os.path.exists('data_log'):
				os.makedirs('data_log')
			fname = str(today) + 'POWER.log'  # log file to save data in
			fdirectory = '/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m")
			fmode = 'a'  # log file mode = append
			if not os.path.exists(fdirectory):
				os.makedirs(fdirectory)
			outf = open(os.path.join(fdirectory, fname), fmode)
			outf.write(x)  # write line of text to file
			outf.flush()  # make sure it actually gets written out
		except Exception:
			print("DATA LOG ERROR", today, now, buffer)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
		if emoncms_update:
			try:
				url = 'https://emoncms.org/input/post.json?node=%s&json={CTT:%s,CT1:%s,CT2:%s,CT3:%s,CT4:%s,VOLT:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, cttotal, ct1p, ct2p, ct3p, ct4p, volt)
				r = requests.post(url, timeout=req_timeout)
				if verbose == 'true':
					print(r.text)
					if "ok" in r:
						print("EMONCMS Update OK", r)
					else:
						print("EMCONMS Update FAILED", r)
			except requests.exceptions.RequestException:
				print("EMONCMS REQUESTS ERROR", today, now, buffer)
				traceback.print_exc(file=sys.stdout)
				print('-' * 60)
			except Exception:
				print("EMONCMS GENERAL ERROR", today, now, buffer)
				traceback.print_exc(file=sys.stdout)
				print('-' * 60)
