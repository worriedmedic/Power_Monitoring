#!/bin/sh

cd /home/pi/Power_Monitoring
python Power_Monitor.py >> /home/pi/Power_Monitoring/data_log/Power_Monitor.log 2>&1
