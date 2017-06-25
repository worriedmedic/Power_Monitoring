#!/bin/sh

if [ ! -d "/home/pi/Power_Monitoring/data_log" ]; then
  mkdir /home/pi/Power_Monitoring/data_log
fi

sleep 5
python /home/pi/Power_Monitoring/Gateway_Logger.py -vv >> /home/pi/Power_Monitoring/data_log/Gateway_Logger.log 2>&1
