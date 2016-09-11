#!/bin/bash

cd /home/pi/Power_Monitoring/output

pngcrush -c 0 -ow 00_01_Temp.png
sudo cp -f 00_01_Temp.png /var/www/html/
sudo chmod 755 /var/www/html/00_01_Temp.png
