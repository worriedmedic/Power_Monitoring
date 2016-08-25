#!/bin/bash
# Script to restart the computer if there is no internet connection 
#   within the next 10 minutes of whenever the script is run, which 
#   I'll setup via crontab to run every half an hour. 

IS=`/bin/ping -c 5 8.8.8.8 | grep -c "64 bytes"`        

if (test "$IS" -gt "2") then                                
        internet_conn="1"
    exit
else
    internet_conn="0"
    sleep 600

    AA=`/bin/ping -c 5 74.125.226.18 | grep -c "64 bytes"`

    if (test "$AA" -gt "2") then                                
        internet_conn="1"
        exit
    else
        sudo shutdown -r now
    fi
fi
