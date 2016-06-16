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
verbose             = 'true'

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

        addr  = buffer[0:2]

        if addr.startswith('0'):
            buffer.split(',')
            temp = buffer.split(',')[1].strip('T')
            press = buffer.split(',')[2].strip('P')
            humid = buffer.split(',')[3].strip('H')
            light = buffer.split(',')[4].strip('L')
            volt = buffer.split(',')[5].strip('V')
            rssi = buffer.split(',')[6].strip('\n')
            
            ### Check output of above split ###
            #print(temp,press,humid,volt,light,rssi) 
            
        if txt_logging == 'true':
            fname = str(today) + '.log'  # log file to save data in
            fdirectory = 'data_log'
            fmode = 'a'  # log file mode = append

            if not os.path.exists(fdirectory):
                os.makedirs(fdirectory)

            outf = open(os.path.join(fdirectory, fname), fmode)
            outf.write(x)  # write line of text to file
            outf.flush()  # make sure it actually gets written out

        if thingspeak_update == 'true':
            url = 'https://api.thingspeak.com/update.json'

            if addr == '00': #
                api_key = 'TFGVV0YYM18ALONJ'
                temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': light, 'field6': volt, 'field7': rssi}
                r = requests.post(url,data=temp_payload)
                if verbose == 'true':
                    print(r.text)

            elif addr == '01':
                api_key = 'ARPQ7GWOHTQSYWYW'
                temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': light, 'field6': volt, 'field7': rssi}
                r = requests.post(url, data=temp_payload)
                if verbose == 'true':
                    print(r.text)
            
            elif addr == '06':
                api_key = 'LZAFORDCZ4UT75GU'
                temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': light, 'field6': volt, 'field7': rssi}
                r = requests.post(url, data=temp_payload)
                if verbose == 'true':
                    print(r.text)
                    
            elif addr == '07':
                api_key = 'NQQZE8CL8ZC445DN'
                temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': light, 'field6': volt, 'field7': rssi}
                r = requests.post(url, data=temp_payload)
                if verbose == 'true':
                    print(r.text)
            
            elif addr == '08':
                api_key = '8SHTGBFETA4XVN5P'
                temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': light, 'field6': volt, 'field7': rssi}
                r = requests.post(url, data=temp_payload)
                if verbose == 'true':
                    print(r.text)

            elif addr == '09':
                api_key = 'TUFQWU8SA1HL1B4O'
                temp_payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid, 'field5': light, 'field6': volt, 'field7': rssi}
                r = requests.post(url, data=temp_payload)
                if verbose == 'true':
                    print(r.text)

            elif addr == 'A1':
                api_key = '2I106Q4EPCT9228E'
                power_payload = {'api_key': api_key, 'field1': addr, 'field2': watts, 'field4': volt, 'field5': rssi}
                r = requests.post(url, data=power_payload)
                if verbose == 'true':
                    print(r.text)

            else:
                print("SENSOR ID NOT FOUND")
        
        if emoncms_update == 'true':
            url = 'https://emoncms.org/input/post.json?node=%s&json={T:%s,P:%s,H:%s,L:%s,V:%s,R:%s}&apikey=4e6eff5d047580696f0e2a7ae9323983' % (addr, temp, press, humid, light, volt, rssi)
            r = requests.post(url)
            if verbose == 'true':
                if "ok" in r:
                    print("EMONCMS Update OK")
                else:
                    print("EMCONMS Update FAILED")
            
