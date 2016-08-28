#!/bin/bash
echo "######################################################################################"
echo "Power_Monitoring install by lwh"
echo "######################################################################################"
echo 
### APT-GET INSTALL DEPENDENCIES
while true; do
    read -p "Which location is this? (dover/cutty) " -n 5 -r
    echo
    case $REPLY in
        [Cu][Uu][Tt][Tt][Yy])
            echo "Setting location as CUTTYHUNK"
            if [ -f 'dover.location' ]; then
                rm dover.location
            else
                echo "'dover.location' not found..."
                echo "Moving on..."
                echo
            fi
            break
            ;;
        [Dd][Oo][Vv][Ee][Rr])
            echo "Setting location as DOVER"
            if [ -f 'cuttyhunk.location' ]; then
                rm cuttyhunk.location
            else
                echo "'cuttyhunk.location' not found..."
                echo "Moving on..."
                echo
            fi
            break
            ;;
        *)
            echo "'cutty' or 'dover' please..."
            echo
            ;;
    esac
done

### APT-GET INSTALL DEPENDENCIES
while true; do
    read -p "Install dependencies (y/n)? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Installing Dependencies..."
        sudo apt-get update
        sudo apt-get install apache2 python-lxml libxml2-dev libxslt-dev python-dev pngcrush librsvg2-bin fail2ban tightvncserver -y
        echo
        break
    elif [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo
        echo "Dependencies NOT installed..."
        echo 
        break
    fi
done

### NGROK
while true; do
    read -p "Install ngrok? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
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
            echo
            break
        else
            echo "Copy of NGROK found in /usr/local/bin/ - moving on..."
            echo
            break
        fi
    elif [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo
        echo "Ngrok NOT installed..."
        echo 
        break
    fi
done

### NETWORK_RESTART.SH
while true; do
    read -p "Install network_restart.sh? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Copying 'network_restart.sh' to /usr/local/bin/"
        sudo cp network_restart.sh /usr/local/bin
        echo
        break
    elif [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo "network_restart.sh NOT installed..."
        echo
        break
    fi
done

### DROPBOX-UPLOADER.SH
while true; do
    read -p "Install dropbox-uploader.sh? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Copying 'Dropbox-Uploader.sh' to /usr/local/bin/"
        sudo cp Dropbox-Uploader/dropbox_uploader.sh /usr/local/bin/
        echo
        break
    elif [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo "dropbox-uploader.sh NOT installed..."
        echo
        break
    fi
done

### CRONTAB ENTRIES
while true; do
    read -p "Install CRONTAB entries? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo
        echo "INSTALLING CRONTAB ENTRIES... Will add necessary entries to existing crontab"
        echo "Even if they're already there..."
        crontab -l > mycron #OUTPUT EXISTING CRONTAB TO FILE
        echo "@reboot /home/pi/Power_Monitoring/Gateway_Logger.sh" >> mycron
        echo "@reboot /home/pi/Power_Monitoring/Power_Monitor.sh" >> mycron
        echo "@reboot /home/pi/Power_Monitoring/SVG_Processing.sh" >> mycron
        echo "@reboot /home/pi/Power_Monitoring/SVG_PNG_Script.sh" >> mycron
        echo "*/10 * * * * /home/pi/Power_Monitoring/tweeter.sh" >> mycron
        echo "*/15 * * * * /home/pi/Power_Monitoring/Dropbox-Uploader/data_log_update.sh" >> mycron
        crontab mycron #WRITE ADDITIONS TO CRONTAB
        rm mycron #CLEAN UP
        echo
        echo "PLEASE ADD THE FOLLOWING LINES TO /etc/crontab as no good scripted way to add them exists..."
        echo "*/5 *   * * *   root    /usr/local/bin/network_restart.sh >> /var/log/network_restart.log 2>&1"
        echo "@reboot         pi      ngrok start -all > /dev/null"
        break
    elif [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo "CRONTAB entires not installed..."
        echo
        break
    fi
done
