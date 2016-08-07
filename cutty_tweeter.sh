#!/bin/sh

sleep 2
cd /home/pi/Power_Monitoring
python cutty_tweeter.py > /home/pi/Power_Monitoring/data_log/cutty_tweeter.log 2>&1
