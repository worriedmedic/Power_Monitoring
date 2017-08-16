#!/bin/sh
cd /home/pi/Power_Monitoring
export DISPLAY=:0
python display.py >> ./data_log/display.log 2>&1
