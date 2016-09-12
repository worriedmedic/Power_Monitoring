#!/bin/bash

sleep 20 #Give the python script time to output the images...

cd /home/pi/Power_Monitoring/output

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  pngcrush -reduce -brute -l 9 -ow plot_temp_16.png
  pngcrush -reduce -brute -l 9 -ow plot_press_16.png
  pngcrush -reduce -brute -l 9 -ow plot_humid_16.png
  sudo cp -f plot_temp_16.png plot_press_16.png plot_humid_16.png /var/www/html/
  sudo chmod 755 /var/www/html/plot_temp_16.png /var/www/html/plot_press_16.png /var/www/html/plot_humid_16.png
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  pngcrush -c 0 -ow plot_temp_16.png
  pngcrush -c 0 -ow plot_press_16.png
  pngcrush -c 0 -ow plot_humid_16.png
  sudo cp -f plot_temp_16.png plot_press_16.png plot_humid_16.png /var/www/html/
  sudo chmod 755 /var/www/html/plot_temp_16.png /var/www/html/plot_press_16.png /var/www/html/plot_humid_16.png
fi

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload plot_temp_16.png plot_press_16.png plot_humid_16.png /Programming/logs/dover/plots/
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload plot_temp_16.png plot_press_16.png plot_humid_16.png /Programming/logs/cuttyhunk/plots/
fi
