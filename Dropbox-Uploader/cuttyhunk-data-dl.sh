#!/bin/bash

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -s -p download /Programming/logs/cuttyhunk/ ~/Power_Monitoring/
  sudo cp /home/pi/Power_Monitoring/cuttyhunk/weather_output.txt /var/www/html/cutty/
  sudo cp /home/pi/Power_Monitoring/cuttyhunk/weather-script-output.png /var/www/html/cutty/
  sudo cp /home/pi/Power_Monitoring/cuttyhunk/weather-script-output.svg /var/www/html/cutty/
  sudo cp /home/pi/Power_Monitoring/cuttyhunk/plots/* /var/www/html/cutty/
  sudo chmod 755 /var/www/html/cutty/*
fi
