#!/bin/sh
#FOR BLANK SYSTEM INSTALL OF THE FOLLOWING PACKAGES
#ALL ARE REQUIRED FOR POWER_MONITORING
#apache2
#python-lxml
#libxml2-dev
#libxslt-dev
#python-dev
#tightvncvserver
#fail2ban
#pngcrush
#librsvg2-bin

sudo apt-get update
sudo apt-get install apache2 python-lxml libxml2-dev libxslt-dev python-dev pngcrush librsvg2-bin fail2ban tightvncserver -y

