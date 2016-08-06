#!/bin/sh
#Script to update log files to dropbox

/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh -p upload ~/Power_Monitoring/data_log/ /Programing/
/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh -p upload /var/log/network_restart.log /Programing/data_log/

find /home/pi/Power_Monitoring/data_log/* -mtime +7 -delete
