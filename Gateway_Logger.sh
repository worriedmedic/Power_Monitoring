#!/bin/sh

cd /home/pi/Power_Monitoring
python Gateway_Logger.py >> /home/pi/Power_Monitoring/data_log/Gateway_Logger.log 2>&1

