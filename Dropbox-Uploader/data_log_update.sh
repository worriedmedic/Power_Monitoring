#!/bin/sh
#Script to update log files to dropbox

if [ ! -d "/home/pi/Power_Monitoring/data_archive" ]; then
  mkdir /home/pi/Power_Monitoring/data_archive
fi

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programming/dover/
  /home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh -p upload /var/log/network_restart.log /Programming/dover/data_log/
  
  find /home/pi/Power_Monitoring/data_log/* -mtime +2 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +2 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
  
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programming/
  /home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh -p upload /var/log/network_restart.log /Programming/data_log/
  
  find /home/pi/Power_Monitoring/data_log/* -mtime +7 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +7 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
  
fi
