#!/bin/sh

if [ ! -d "/home/pi/Power_Monitoring/data_log" ]; then
  mkdir /home/pi/Power_Monitoring/data_log
fi

python /home/pi/Power_Monitoring/Power_Monitor.py >> /home/pi/Power_Monitoring/data_log/Power_Monitor.log 2>&1
