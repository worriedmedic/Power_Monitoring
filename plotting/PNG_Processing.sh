#!/bin/bash

sleep 5 #Give the python script time to output the images...

cd /home/pi/Power_Monitoring/output

#if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  #pngcrush -reduce -brute -l 9 -ow plot_temp.png
  #pngcrush -reduce -brute -l 9 -ow plot_press.png
  #pngcrush -reduce -brute -l 9 -ow plot_humid.png
  #pngcrush -reduce -brute -l 9 -ow plot_volt.png
  #pngcrush -reduce -brute -l 9 -ow plot_rssi.png
  #sudo cp -f plot_temp.png plot_press.png plot_humid.png plot_volt.png plot_rssi.png 3Hpower.png 24Hpower.png 7Dpower.png /var/www/html/
  #sudo chmod 755 /var/www/html/plot_temp.png /var/www/html/plot_press.png /var/www/html/plot_humid.png /var/www/html/plot_volt.png /var/www/html/plot_rssi.png /var/www/html/3Hpower.png /var/www/html/24Hpower.png /var/www/html/7Dpower.png
#elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  #pngcrush -c 0 -ow plot_temp.png
  #pngcrush -c 0 -ow plot_press.png
  #pngcrush -c 0 -ow plot_humid.png
  #pngcrush -c 0 -ow plot_volt.png
  #pngcrush -c 0 -ow plot_rssi.png
  #sudo cp -f plot_temp.png plot_press.png plot_humid.png plot_volt.png plot_rssi.png /var/www/html/
  #sudo chmod 755 /var/www/html/plot_temp.png /var/www/html/plot_press.png /var/www/html/plot_humid.png /var/www/html/plot_volt.png /var/www/html/plot_rssi.png
#fi

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload plot_temp.png plot_press.png plot_humid.png plot_volt.png plot_rssi.png 3Hpower.png 24Hpower.png 7Dpower.png /Programming/logs/dover/plots/
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload plot_temp.png plot_press.png plot_humid.png plot_volt.png plot_rssi.png /Programming/logs/cuttyhunk/plots/
fi
