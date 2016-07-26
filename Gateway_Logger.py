#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

from __future__ import print_function
import serial, io
import time
import datetime
import requests
import os.path

addr                = '/dev/ttyUSB0'  # serial port to read data from
baud                = 9600   # baud rate for serial port
thingspeak_update   = 'true' # Turn on/off updating to ThingSpeak
emoncms_update      = 'true' # Turn on/off updating to Emoncms
txt_logging         = 'true' # Enable/Disable logging to TXT file
verbose             = 'false'

with serial.Serial(addr,9600) as pt:
    try:
        spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1), encoding='ascii', errors='ignore',line_buffering=True)
        spb.readline()  # throw away first 3 lines; likely to start mid-sentence (incomplete)
        spb.readline()
        spb.readline()
    except Exception as e:
        print("SERIAL READ ERROR", e)

    while (1):
        now = time.strftime("%H:%M:%S") # Call time of serial read
        today = datetime.date.today() # Call date of serial read

        try:
            buffer = spb.readline()  # read one line of text from serial port
            buffer = buffer.strip("\n")
            
        except Exception as e:
            print("SERIAL READ ERROR", today, now, e)

        x = str(today) + ',' + str(now) + ',' + str(buffer)

        if verbose == 'true':
            print (x,end='')    # echo line of text on-screen

        try:
            addr  = buffer[0:2]
        except Exception as e:
            print("ADDRESS ERROR", today, now, e, "::", buffer)


        if addr.startswith('0'):
            try:
                buffer.split(',')
                temp = buffer.split(',')[1].strip('T')
                press = buffer.split(',')[2].strip('P')
                humid = buffer.split(',')[3].strip('H')
                volt = buffer.split(',')[4].strip('V')
                rssi = buffer.split(',')[5]
            except Exception as e:
                print("DATA SPLIT ERROR", today, now, e, "::", buffer)
            
        if txt_logging == 'true':
            try:
                fname = str(today) + '.log'  # log file to save data in
                fdirectory = 'data_log/' + time.strftime("%Y-%m")
                fmode = 'a'  # log file mode = append

                if not os.path.exists(fdirectory):
                    os.makedirs(fdirectory)

                outf = open(os.path.join(fdirectory, fname), fmode)
                outf.write(x)  # write line of text to file
                outf.flush()  # make sure it actually gets written out
            except Exception as e:
                print("DATA LOG ERROR", today, now, e, "::", buffer)

        if emoncms_update == 'true':
            try:
                url = 'https://emoncms.org/input/post.json?node=%s&json={T:%s,P:%s,H:%s,V:%s,R:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, temp, press, humid, volt, rssi)
                r = requests.post(url)
                if verbose == 'true':
                    print(r.text)
                    if "ok" in r:
                        print("EMONCMS Update OK")
                    else:
                        print("EMCONMS Update FAILED")
                        
            except requests.exceptions.RequestException as e:
                print("EMONCMS REQUESTS ERROR", today, now, e, "::", buffer)
            except Exception as e:
                print("EMONCMS GENERAL ERROR", today, now, e, "::", buffer)
        
        if thingspeak_update == 'true':
            url = 'https://api.thingspeak.com/update.json'
            if addr == '00':
                try:
                    api_key = 'TFGVV0YYM18ALONJ'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url,data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)
            
            elif addr == '01':
                try:
                    api_key = 'ARPQ7GWOHTQSYWYW'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)

            elif addr == '05':
                try:
                    api_key = '89NM6222ST0UW15H'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)
                        
            elif addr == '06':
                try:
                    api_key = 'LZAFORDCZ4UT75GU'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)
            
            elif addr == '07':
                try:
                    api_key = 'NQQZE8CL8ZC445DN'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)
            
            elif addr == '08':
                try:
                    api_key = '8SHTGBFETA4XVN5P'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)
            
            elif addr == '09':
                try:
                    api_key = 'TUFQWU8SA1HL1B4O'
                    temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field6': volt, 'field7': rssi}
                    r = requests.post(url, data=temp_payload)
                    if verbose == 'true':
                        print(r.text)
                        if r.text == "0":
                            print("Thingspeak Update FAILED")
                        else:
                            print("Thingspeak Update OK")
                            
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS ERROR", today, now, e, "::", buffer)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR", today, now, e, "::", buffer)
            
            else:
                print("NOT PUSHED TO THINGSPEAK :: SENSOR ID NOT FOUND")
