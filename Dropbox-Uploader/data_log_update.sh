#!/bin/bash
#Script to update log files to dropbox

if [ ! -d '/home/pi/Power_Monitoring/data_archive' ]; then
  mkdir /home/pi/Power_Monitoring/data_archive
fi

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programming/logs/dover/
  dropbox_uploader.sh -p upload /var/log/network_restart.log /Programming/logs/dover/data_log/sys_log/
  dropbox_uploader.sh -p upload /var/log/fail2ban.log /Programming/logs/dover/data_log/sys_log/
  dropbox_uploader.sh -p upload ~/.ngrok2/_ngrok.log /Programming/logs/dover/data_log/sys_log/
  dropbox_uploader.sh -p upload ~/.vnc/raspberrypi\:1.log /Programming/logs/dover/data_log/sys_log/ 
  find /home/pi/Power_Monitoring/data_log/* -mtime +8 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +8 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
  dropbox_uploader.sh -p download /Programming/logs/cuttyhunk/ ~/Power_Monitoring/cutty
  sudo cp /home/pi/Power_Monitoring/cutty/weather_output.txt /var/www/html/cutty/
  sudo cp /home/pi/Power_Monitoring/cutty/weather-script-output.png /var/www/html/cutty/
  sudo cp /home/pi/Power_Monitoring/cutty/weather-script-output.svg /var/www/html/cutty/
  sudo cp /home/pi/Power_Monitoring/cutty/plots/* /var/www/html/cutty/
  sudo chmod 755 /var/www/html/cutty/*
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/* /Programming/logs/cuttyhunk/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/network_restart.log /Programming/logs/cuttyhunk/data_log/sys_log/network_restart.log
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/fail2ban.log /Programming/logs/cuttyhunk/data_log/sys_log/fail2ban.log
  /usr/local/bin/dropbox_uploader.sh -p upload ~/.ngrok2/ngrok.log /Programming/logs/cuttyhunk/data_log/ngrok.log
  /usr/local/bin/dropbox_uploader.sh -p upload ~/.vnc/raspberrypi\:1.log /Programming/logs/cuttyhunk/data_log/sys_log/raspberrypi\:1.log
  find /home/pi/Power_Monitoring/data_log/* -mtime +7 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +7 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
fi
