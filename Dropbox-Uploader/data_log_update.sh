#!/bin/bash
#Script to update log files to dropbox

if [ ! -d '/home/pi/Power_Monitoring/data_archive' ]; then
  mkdir /home/pi/Power_Monitoring/data_archive
fi

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programming/logs/dover/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/network_restart.log /Programming/logs/dover/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/fail2ban.log /Programming/logs/dover/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/syslog /Programming/logs/dover/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/dmesg /Programming/logs/dover/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload ~/.ngrok2/_ngrok.log /Programming/logs/dover/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload ~/.vnc/raspberrypi\:1.log /Programming/logs/dover/data_log/sys_log/
  
  find /home/pi/Power_Monitoring/data_log/* -mtime +2 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +2 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
  
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programming/logs/cuttyhunk/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/network_restart.log /Programming/logs/cuttyhunk/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/fail2ban.log /Programming/logs/cuttyhunk/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/syslog /Programming/logs/cuttyhunk/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload /var/log/dmesg /Programming/logs/cuttyhunk/data_log/sys_log/
  /usr/local/bin/dropbox_uploader.sh -p upload ~/.ngrok2/_ngrok.log /Programming/logs/cuttyhunk/data_log/
  /usr/local/bin/dropbox_uploader.sh -p upload ~/.vnc/raspberrypi\:1.log /Programming/logs/cuttyhunk/data_log/sys_log/
  
  find /home/pi/Power_Monitoring/data_log/* -mtime +7 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +7 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
  
fi
