#!/bin/bash

cd /home/pi/Power_Monitoring/output

pngcrush -c 0 -ow plot_temp.png
pngcrush -c 0 -ow plot_press.png
pngcrush -c 0 -ow plot_humid.png
sudo cp -f plot_temp.png plot_press.png plot_humid.png /var/www/html/
sudo chmod 755 /var/www/html/plot_temp.png /var/www/html/plot_press.png /var/www/html/plot_humid.png

/usr/local/bin/dropbox_uploader.sh upload -p plot_temp.png plot_press.png plot_humid.png /Programming/logs/cuttyhunk/
