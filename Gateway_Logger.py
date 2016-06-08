#!/usr/bin/python
# get lines of text from serial port, save them to a file, upload to ThingSpeak
# Base source (highly modified): https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

from __future__ import print_function
import serial, io
import time
import datetime
import requests
import os.path

addr                = '/dev/tty.usbserial-A104VAFG'  # serial port to read data from
baud                = 9600            # baud rate for serial port
thingspeak_update   = 'true' # 'true' or 'false' to turn on/off updating to ThingSpeak
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
            temp  = buffer[4:9]
            press = buffer[11:16]
            humid = buffer[18:23]
            volt  = buffer[25:30]
            rssi  = buffer[31:34]

        elif addr.startswith('A'):
            buffer.split(',')
            total_watts = buffer.split(',')[1].strip('TW')
            watts = buffer.split(',')[2].strip('WC')
            avg_watts = buffer.split(',')[3].strip('AW')
            volt = buffer.split(',')[4].strip('V')
            rssi = buffer.split(',')[5].strip('\n')



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

            if addr == '00':
                api_key = 'TFGVV0YYM18ALONJ'
                payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid,
                       'field5': volt, 'field6': rssi}
                r = requests.post(url,data=payload)
                if verbose == 'true':
                    print(r.text)

            elif addr == '01':
                api_key = 'ARPQ7GWOHTQSYWYW'
                payload = {'api_key': api_key, 'field1': addr, 'field2': temp, 'field3': press, 'field4': humid,
                       'field5': volt, 'field6': rssi}
                r = requests.post(url, data=payload)
                if verbose == 'true':
                    print(r.text)

            elif addr == 'A1':
                api_key = '2I106Q4EPCT9228E'
                payload = {'api_key': api_key, 'field1': total_watts, 'field2': watts, 'field3': avg_watts, 'field4': volt, 'field5': rssi}
                r = requests.post(url, data=payload)
                if verbose == 'true':
                    print(r.text)

            else:
                print("SENSOR ID NOT FOUND")