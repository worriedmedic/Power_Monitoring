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
    spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1),
        encoding='ascii', errors='ignore',line_buffering=True)
    spb.readline()  # throw away first line; likely to start mid-sentence (incomplete)
    spb.readline()
    spb.readline()

    while (1):
        now = time.strftime("%H:%M:%S") # Call time of serial read
        today = datetime.date.today() # Call date of serial read

        buffer = spb.readline()  # read one line of text from serial port

        x = str(today) + ',' + str(now) + ',' + str(buffer)

        print (x,end='')    # echo line of text on-screen

        addr = '10'
        
        buffer.split(' ')
        ct1p = buffer.split(' ')[0]
        ct2p = buffer.split(' ')[1]
        ct3p = buffer.split(' ')[2]
        ct4p = buffer.split(' ')[3]
        volt = buffer.split(' ')[4]
        
        volt = float(volt) / 100
            
        ### Check output of above split ###
        print(ct1p,ct2p,ct3p,ct4p,volt) 
            
        if txt_logging == 'true':
            fname = str(today) + 'POWER.log'  # log file to save data in
            fdirectory = 'data_log'
            fmode = 'a'  # log file mode = append

            if not os.path.exists(fdirectory):
                os.makedirs(fdirectory)

            outf = open(os.path.join(fdirectory, fname), fmode)
            outf.write(x)  # write line of text to file
            outf.flush()  # make sure it actually gets written out

        if thingspeak_update == 'true':
            url = 'https://api.thingspeak.com/update.json'

            if addr == '10':
                api_key = '2I106Q4EPCT9228E'
                power_payload = {'api_key': api_key, 'field1': ct1p, 'field2': ct2p, 'field3': ct3p, 'field4': ct4p, 'field5': volt}
                r = requests.post(url, data=power_payload)
                if r.text == "0":
                    print("Thingspeak Update FAILED")
                else:
                    print("Thingspeak Update OK")
                    
                if verbose == 'true':
                    print(r.text)

            else:
                print("SENSOR ID NOT FOUND")
        
        if emoncms_update == 'true':
            url = 'https://emoncms.org/input/post.json?node=%s&json={CT1:%s,CT2:%s,CT3:%s,CT4:%s,VOLT:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, ct1p, ct2p, ct3p, ct4p, volt)
            r = requests.post(url)
            if verbose == 'true':
                if "ok" in r:
                    print("EMONCMS Update OK")
                else:
                    print("EMCONMS Update FAILED")