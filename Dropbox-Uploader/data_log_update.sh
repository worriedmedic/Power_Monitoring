#!/bin/bash
#Script to update log files to dropbox

if [ ! -d '/home/pi/Power_Monitoring/data_archive' ]; then
  mkdir /home/pi/Power_Monitoring/data_archive
fi

if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programming/logs/dover/
  find /home/pi/Power_Monitoring/data_log/* -mtime +8 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +8 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
  /usr/local/bin/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/* /Programming/logs/cuttyhunk/
  find /home/pi/Power_Monitoring/data_log/* -mtime +4 -exec cp {} /home/pi/Power_Monitoring/data_archive/  \; #Copies any files older than 7 days old to an archive location
  find /home/pi/Power_Monitoring/data_log/* -mtime +4 -delete #Deletes files older than 7 days to prevent extensive dropbox uploads
  find /home/pi/Power_Monitoring/data_log/* -type d -empty -delete #Deletes empty directories left over
fi
