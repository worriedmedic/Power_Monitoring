#!/bin/sh

sleep 2
cd /home/pi/Power_Monitoring
python tweeter.py > /home/pi/Power_Monitoring/data_log/tweeter.log 2>&1
