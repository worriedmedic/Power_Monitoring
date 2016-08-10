#!/bin/sh

if [ ! -d "/home/pi/Power_Monitoring/data_log" ]; then
  mkdir /home/pi/Power_Monitoring/data_log
fi

cd /home/pi/Power_Monitoring
python SVG_Processing.py >> /home/pi/Power_Monitoring/data_log/SVG_Processing.log 2>&1
