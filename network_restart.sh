#!/bin/bash
##################################################################
# "Borrowed" from author bellow (thanks) and modified for 
# specific use.
# Author:    Kevin Reed (Dweeber)
# Copyright: Copyright (c) 2012 Kevin Reed <kreed@tnet.com>
#            https://github.com/dweeber/WiFi_Check
##################################################################
# Settings
# Where and what you want to call the Lockfile
lockfile='/var/run/WiFi_Check.pid'
# Which Interface do you want to check/fix
wlan='wlan0'
SERVER='8.8.8.8'
##################################################################
date | tr -d '\n'

# Check to see if there is a lock file
if [ -e $lockfile ]; then
    # A lockfile exists... Lets check to see if it is still valid
    pid=`cat $lockfile`
    if kill -0 &>1 > /dev/null $pid; then
        # Still Valid... lets let it be...
        echo -n " Process still running, Lockfile valid"
        exit 1
    else
        # Old Lockfile, Remove it
        # echo "Old lockfile, Removing Lockfile"
        rm $lockfile
    fi
fi
# If we get here, set a lock file using our current PID#
# echo "Setting Lockfile"
echo $$ > $lockfile

# We can perform check
# echo "Performing Network check for $wlan"

if ifconfig $wlan | grep -q "inet addr:"; then
    echo -n " ifconfig up,"
    ifconfig $wlan | grep -o -E '.{0,10}inet addr:.{0,10}' | tr -d ' ' | tr -d '\n'
else
    echo -n " ifconfig down,"
    ifdown $wlan
    sleep 5
    ifup --force $wlan
    sleep 5
    ifconfig $wlan | grep -o -E '.{0,10}inet addr:.{0,10}' | tr -d ' ' | tr -d '\n'
fi

# echo "Pining $SERVER"
ping -c2 $SERVER > /dev/null

if [ $? != 0 ] ; then
    # Restart the wireless interface
    echo -n " WAN down,"
    ifdown --force $wlan
    sleep 5
    ifup --force $wlan
    sleep 5
    ifconfig $wlan | grep -o -E '.{0,10}inet addr:.{0,10}' | tr -d ' ' | tr -d '\n'
else
    echo " WAN up,"
    
fi

# echo "Current Setting:"
# ifconfig $wlan | grep "inet addr:"
 
# Check is complete, Remove Lock file and exit
# echo "process is complete, removing lockfile"
rm $lockfile
exit 0
