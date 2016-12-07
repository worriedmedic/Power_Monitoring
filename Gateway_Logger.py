#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

from __future__ import print_function
import serial, io
import time
import datetime
import requests
import os.path
import traceback
import sys

baud                = 9600   # baud rate for serial port
thingspeak_update   = True # Turn on/off updating to ThingSpeak
emoncms_update      = True # Turn on/off updating to Emoncms
txt_logging         = True # Enable/Disable logging to TXT file
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
	elif arg == '-h':
		print("Gateway_Logger.py script - LWH & NHH")
		print("Backend processing of data collected by Arduino based sensors for output to SVG/PNG file")
		print("Options:  [-e EMONCMS UPDATING ON (default)] [-l LOGGING TO FILE (default)]")
		print("[-t THINGSPEAK UPDATING ON (default)] [-v VERBOSE] [-h HELP]")
		sys.exit()
	
if os.path.isfile('dover.location'):
    addr = '/dev/ttyUSB0'
elif os.path.isfile('cuttyhunk.location'):
    addr = '/dev/ttyACM0'

with serial.Serial(addr,9600, timeout=300) as pt:
    try:
        spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1), encoding='ascii', errors='strict',line_buffering=True)
        spb.readline()
        spb.readline()
        spb.readline()
    except Exception:
        print("SERIAL READ ERROR")
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

    while (1):
        now = time.strftime("%H:%M:%S") # Call time of serial read
        today = datetime.date.today() # Call date of serial read

        try:
            buffer = spb.readline()  # read one line of text from serial port
            buffer = buffer.strip("\n")
            
        except Exception:
            print("SERIAL READ ERROR", today, now)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

        x = str(today) + ',' + str(now) + ',' + str(buffer) + '\n'

        if verbose:
            print (x,end='')    # echo line of text on-screen

        try:
            addr  = buffer[0:2]
        except Exception:
            print("ADDRESS ERROR", today, now, buffer)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)


        if addr.startswith('0'):
            try:
                buffer.split(',')
                temp = buffer.split(',')[1].strip('T')
                press = buffer.split(',')[2].strip('P')
                humid = buffer.split(',')[3].strip('H')
                volt = buffer.split(',')[4].strip('V')
                rssi = buffer.split(',')[5]
                
                dew = float(temp) - (0.36 * (100 - float(humid))) ##FROM DATA PROCESSING PYTHON SCRIPT
                
            except Exception:
                print("DATA SPLIT ERROR", today, now, buffer)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
            
        if txt_logging:
            try:
                if not os.path.exists('data_log'):
                    os.makedirs('data_log')
                
                fname = str(today) + '.log'  # log file to save data in
                fdirectory = 'data_log/' + time.strftime("%Y-%m")
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
                url = 'https://emoncms.org/input/post.json?node=%s&json={T:%s,P:%s,H:%s,V:%s,R:%s,D:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, temp, press, humid, volt, rssi, dew)
                r = requests.post(url, timeout=req_timeout)
                if verbose:
                    print(r.text)
                    if "ok" in r:
                        print("EMONCMS Update OK")
                    else:
                        print("EMCONMS Update FAILED")
                        
            except requests.exceptions.Timeout:
            	print("REQUESTS TIMEOUT ERROR", today, now, buffer)
            	print('-' * 60)
            except requests.exceptions.RequestException:
                print("EMONCMS REQUESTS ERROR", today, now, buffer)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
            except Exception:
                print("EMONCMS GENERAL ERROR", today, now, buffer)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        
        if thingspeak_update:
            url = 'https://api.thingspeak.com/update.json'
            if addr == '00':
                try:
                    api_key = 'TFGVV0YYM18ALONJ'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url,data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
            		print("REQUESTS TIMEOUT ERROR", today, now, buffer)
            		print('-' * 60)
                except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            
            elif addr == '01':
                try:
                    api_key = 'ARPQ7GWOHTQSYWYW'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
            		print("REQUESTS TIMEOUT ERROR", today, now, buffer)
            		print('-' * 60)
            	except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)

            elif addr == '02':
                try:
                    api_key = 'GVWSJ8V12MIPJBLY'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
            		print("REQUESTS TIMEOUT ERROR", today, now, buffer)
            		print('-' * 60)
            	except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            
            elif addr == '03':
                try:
                    api_key = 'DOXY1Q9I6C6I88DA'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
					print("REQUESTS TIMEOUT ERROR", today, now, buffer)
					print('-' * 60)
            	except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)

            elif addr == '04':
                try:
                    api_key = 'MJEV3AA82GKVMP4V'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
			print("REQUESTS TIMEOUT ERROR", today, now, buffer)
			print('-' * 60)
		except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                    
            elif addr == '05':
                try:
                    api_key = '89NM6222ST0UW15H'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
			print("REQUESTS TIMEOUT ERROR", today, now, buffer)
			print('-' * 60)
		except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                        
            elif addr == '06':
                try:
                    api_key = 'LZAFORDCZ4UT75GU'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
			print("REQUESTS TIMEOUT ERROR", today, now, buffer)
			print('-' * 60)
		except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            
            elif addr == '07':
                try:
                    api_key = 'NQQZE8CL8ZC445DN'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
			print("REQUESTS TIMEOUT ERROR", today, now, buffer)
			print('-' * 60)
		except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            
            elif addr == '08':
                try:
                    api_key = '8SHTGBFETA4XVN5P'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
			print("REQUESTS TIMEOUT ERROR", today, now, buffer)
			print('-' * 60)
		except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            
            elif addr == '09':
                try:
                    api_key = 'TUFQWU8SA1HL1B4O'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': dew, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload, timeout=req_timeout)
                    if verbose:
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.Timeout:
			print("REQUESTS TIMEOUT ERROR", today, now, buffer)
			print('-' * 60)
		except requests.exceptions.RequestException:
                    print("THINGSPEAK REQUESTS ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
                except Exception:
                    print("THINGSPEAK GENERAL ERROR", today, now, buffer)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            
            else:
                print("NOT PUSHED TO THINGSPEAK :: SENSOR ID NOT FOUND", today, now, buffer)
