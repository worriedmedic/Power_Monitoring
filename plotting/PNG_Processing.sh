#!/bin/bash

sleep 20 #Give the python script time to output the images...

cd /home/pi/Power_Monitoring/output

pngcrush -c 0 -ow plot_temp.png
pngcrush -c 0 -ow plot_press.png
pngcrush -c 0 -ow plot_humid.png
sudo cp -f plot_temp.png plot_press.png plot_humid.png /var/www/html/
sudo chmod 755 /var/www/html/plot_temp.png /var/www/html/plot_press.png /var/www/html/plot_humid.png

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload plot_temp.png plot_press.png plot_humid.png /Programming/logs/cuttyhunk/plots/
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload plot_temp.png plot_press.png plot_humid.png /Programming/logs/cuttyhunk/plots/
fi
