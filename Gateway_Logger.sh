#!/bin/sh
if [ ! -d "/home/pi/Power_Monitoring/data_log" ]; then
  mkdir /home/pi/Power_Monitoring/data_log
fi
cd /home/pi/Power_Monitoring
python Gateway_Logger.py >> /home/pi/Power_Monitoring/data_log/Gateway_Logger.log 2>&1
