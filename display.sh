#!/bin/sh
cd /home/pi/Power_Monitoring
sleep 10
export DISPLAY=:0
python display.py >> /home/pi/Power_Monitoring/data_log/display.log 2>&1
