#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

#from __future__ import print_function
import serial, io
import time
import datetime
import requests
import os.path
import traceback
import sys

baud                = 9600   # baud rate for serial port
emoncms_update      = True # Turn on/off updating to Emoncms
txt_logging         = True # Enable/Disable logging to TXT file
verbose             = False
verbose_verbose	    = True
thingspeak_update   = False
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

while(True):
	try:
		if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
			addr = '/dev/ttyUSB0'
		elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
			addr = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AL02CC7C-if00-port0'
		pt = serial.Serial(addr,9600, timeout=150)
		spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1), errors='strict',line_buffering=True)
		b1 = spb.readline()
		b2 = spb.readline()
		#b3 = spb.readline()
		serial_present = True
		if verbose:
			print("SERIAL PRESENT", serial_present)
			print(b1, b2)
	except Exception:
		now = time.strftime("%H:%M:%S")
		today = datetime.date.today()
		print("SERIAL INIT ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
		serial_present = False
		time.sleep(10)
	while serial_present:
		now = time.strftime("%H:%M:%S")
		today = datetime.date.today()
		try:
			buffer = spb.readline()
			if verbose_verbose:
				rawout = open('/home/pi/Power_Monitoring/data_log/rawoutput.log', 'a')
				rawout.write(str(today) + ',' + str(now) + ',' + buffer)
				rawout.flush()
			if verbose:
				print(buffer)
		except Exception:
			print("SERIAL READLINE() ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
			pt.close()
			time.sleep(2)
			break
		try:
			buffer = buffer.strip('\n')
			addr = buffer.split(',')[0]
			temp = buffer.split(',')[1].strip('T')
			press = buffer.split(',')[2].strip('P')
			humid = buffer.split(',')[3].strip('H')
			volt = buffer.split(',')[4].strip('V')
			rssi = buffer.split(',')[5]
			dew = float(temp) - (0.36 * (100 - float(humid)))
		except Exception:
			print("DATA PROCESSING ERROR", today, now, "STRING:", buffer, ":END")
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
			pt.close()
			time.sleep(2)
			break
		if txt_logging:
			try:
				x = str(today) + ',' + str(now) + ',' + str(buffer) + '\n'
				if verbose:
					print (x)
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
				print("DATA LOG WRITE ERROR", today, now, buffer)
				traceback.print_exc(file=sys.stdout)
				print('-' * 60)
		if emoncms_update:
			try:
				url = 'https://emoncms.org/input/post.json?node=%s&json={T:%s,P:%s,H:%s,V:%s,R:%s,D:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, temp, press, humid, volt, rssi, dew)
				r = requests.post(url, timeout=req_timeout)
				if verbose:
					print(r.text)
					if "ok" in r:
						print("EMONCMS Update OK")
					else:
						print("EMCONMS Update FAILED")
			except requests.exceptions.Timeout:
				print("REQUESTS GENERAL TIMEOUT ERROR", today, now, buffer)
				print('-' * 60)
			except requests.exceptions.RequestException:
				print("EMONCMS REQUESTS ERROR", today, now, buffer)
				print('-' * 60)
			except Exception:
				print("EMONCMS OTHER GENERAL ERROR", today, now, buffer)
				traceback.print_exc(file=sys.stdout)
				print('-' * 60)
