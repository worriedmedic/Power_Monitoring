#!/bin/bash

echo "INSTALLING CRONTAB ENTRIES... Will add necessary entries to existing crontab"

crontab -l > mycron #OUTPUT EXISTING CRONTAB TO FILE
echo "@reboot /home/pi/Power_Monitoring/Gateway_Logger.sh" >> mycron
echo "@reboot /home/pi/Power_Monitoring/Power_Monitor.sh" >> mycron
echo "@reboot /home/pi/Power_Monitoring/SVG_Processing.sh" >> mycron
echo "@reboot /home/pi/Power_Monitoring/SVG_PNG_Script.sh" >> mycron
echo "*/10 * * * * /home/pi/Power_Monitoring/tweeter.sh" >> mycron
echo "*/15 * * * * /home/pi/Power_Monitoring/Dropbox-Uploader/data_log_update.sh" >> mycron
crontab mycron #WRITE ADDITIONS TO CRONTAB
rm mycron #CLEAN UP
