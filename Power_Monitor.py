#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

from __future__ import print_function
import serial, io
import time
import datetime
import requests
import os.path

addr                = '/dev/ttyUSB1'  # serial port to read data from
baud                = 9600   # baud rate for serial port
thingspeak_update   = 'true' # Turn on/off updating to ThingSpeak
emoncms_update      = 'true' # Turn on/off updating to Emoncms
txt_logging         = 'true' # Enable/Disable logging to TXT file
verbose             = 'false'

with serial.Serial(addr,9600) as pt:
    try:
        spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1), encoding='ascii', errors='ignore',line_buffering=True)
        spb.readline()  # throw away first line; likely to start mid-sentence (incomplete)
        spb.readline()
        spb.readline()
    except Exception as e:
        print(e)

    while (1):
        now = time.strftime("%H:%M:%S") # Call time of serial read
        today = datetime.date.today() # Call date of serial read

        try:
            buffer = spb.readline()  # read one line of text from serial port
        except Exception as e:
            print(e)

        x = str(today) + ',' + str(now) + ',' + str(buffer)

        print (x,end='')    # echo line of text on-screen

        addr = '10'
        
        try:
            buffer.split(' ')
            ct1p = buffer.split(' ')[0]
            ct2p = buffer.split(' ')[1]
            ct3p = buffer.split(' ')[2]
            ct4p = buffer.split(' ')[3]
            volt = buffer.split(' ')[4]
        
            volt = float(volt) / 100
            cttotal = int(ct1p) + int(ct2p)
            
        except Exception as e:
            print("DATA SPLIT ERROR")
            print(e)
            
            ### Check output of above split ###
        if verbose == 'true':
            try:
                print(cttotal,ct1p,ct2p,ct3p,ct4p,volt) 
            except Exception as e:
                print("VERBOSE PRINT ERROR, CHECK DATA SPLIT")
                print(e)
        
        if txt_logging == 'true':
            try:
                fname = str(today) + 'POWER.log'  # log file to save data in
                fdirectory = 'data_log/' + time.strftime("%Y-%m")
                fmode = 'a'  # log file mode = append

                if not os.path.exists(fdirectory):
                    os.makedirs(fdirectory)

                outf = open(os.path.join(fdirectory, fname), fmode)
                outf.write(x)  # write line of text to file
                outf.flush()  # make sure it actually gets written out
            except Exception as e:
                print("DATA LOG ERROR")
                print(e)

        if emoncms_update == 'true':
            try:
                url = 'https://emoncms.org/input/post.json?node=%s&json={CTT:%s,CT1:%s,CT2:%s,CT3:%s,CT4:%s,VOLT:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, cttotal, ct1p, ct2p, ct3p, ct4p, volt)
                r = requests.post(url)
                if "ok" in r:
                    print("EMONCMS Update OK")
                else:
                    print("EMCONMS Update FAILED")
                if verbose == 'true':
                    print(r.text)
            except requests.exceptions.RequestException as e:
                print("EMONCMS REQUESTS FATAL ERROR")
                print(e)
            except Exception as e:
                print("EMONCMS GENERAL ERROR")
                print(e)
                
        if thingspeak_update == 'true':
            url = 'https://api.thingspeak.com/update.json'

            if addr == '10':
                try:
                    api_key = '2I106Q4EPCT9228E'
                    power_payload = {'api_key': api_key, 'field1': cttotal, 'field2': ct1p, 'field3': ct2p, 'field4': ct3p, 'field5': ct4p, 'field6': volt}
                    r = requests.post(url, data=power_payload)
                    if r.text == "0":
                        print("Thingspeak Update FAILED")
                    else:
                        print("Thingspeak Update OK")
                    if verbose == 'true':
                        print(r.text)
                except requests.exceptions.RequestException as e:
                    print("THINGSPEAK REQUESTS FATAL ERROR")
                    print(e)
                except Exception as e:
                    print("THINGSPEAK GENERAL ERROR")
                    print(e)
            
            else:
                print("NOT PUSHED TO THINGSPEAK :: SENSOR ID NOT FOUND")
