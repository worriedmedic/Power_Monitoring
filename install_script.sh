#!/bin/sh
echo "######################################################################################"
echo "Power_Monitoring install by lwh"
echo "######################################################################################"

echo "Do you wish to install dependencies? (apt-get)"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) sudo apt-get update;
        sudo apt-get install apache2 python-lxml libxml2-dev libxslt-dev python-dev pngcrush librsvg2-bin fail2ban tightvncserver -y;
        ;;
        No ) echo "Not Installing Dependencies";;
    esac
done

echo "Checking for NGROK..."
if [ ! -f "/usr/local/bin/ngrok" ]; then
  echo "No copy of NGROK found, installing NGROK"
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
  unzip ngrok-stable-linux-arm.zip
  sudo cp ngrok /usr/local/bin/
  rm ngrok
  rm ngrok-stable-linux-arm.zip
  echo "NEED TO ADD AUTHORIZATION KEY AND ADD SERVICES TO ~/.ngrok2/ngrok.yml"
  echo "authtoken: <AUTHTOKEN>"
  echo "log_level: info"
  echo "log_format: term"
  echo "log: /home/pi/.ngrok2/_ngrok.log"
  echo "tunnels:"
  echo "  ssh:"
  echo "    proto: tcp"
  echo "    addr: 22"
else
  echo "Copy of NGROK found in /usr/local/bin/ - moving on..."
fi

echo "Copying 'network_restart.sh' to /usr/local/bin/"
sudo cp network_restart.sh /usr/local/bin

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

echo "PLEASE ADD THE FOLLOWING LINES TO /etc/crontab as no good scripted way to add them exists..."
echo "*/5 *   * * *   root    /usr/local/bin/network_restart.sh >> /var/log/network_restart.log 2>&1"
echo "@reboot         pi      ngrok start -all > /dev/null"
