#!/bin/sh

cd /home/pi/Power_Monitoring
python SVG_Processing.py >> /home/pi/Power_Monitoring/data_log/SVG_Processing.log 2>&1
