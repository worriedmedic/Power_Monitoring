#Power Monitoring
Homebrew home monitoring project. Includes multiple custom made weather sensors and Open Power Monitoring EmonTX v3 sensor for power usage.

Samelessly borrowing code from andreafabrizi Dropbox-Uploader (https://github.com/andreafabrizi/Dropbox-Uploader/), dweeber WiFi-Check (https://github.com/dweeber/WiFi_Check), thanks!

Weather sensors baised on Arduino Pro Mini (8mhz, 3.3v) with BME280 atmospheric sensor (Temp, Press, Humidity) and Hope RFM95x trancever. Blindly transmits data (q96 sec) with unique ID. Data packets are read by a Arduino Pro Mini (8mhx, 3.3v) and Hope RFM95x transcever, passed on to a RaspberryPi 3 (NOOBS) via USB serial connection where front end processing is handeled in python (Gateway_Logger.py). 

Weather Sensor Data Structure: `00(Address),T99.99(Temp-F),P1000.00(Pressure-hPa),H99.99(Humidity),V99.99(Voltage-%),099(RSSI)`
Sensors seem to stop transmitting when voltage reaches ~81%.

Open Power Monitoring EmonTXv3 modified for US use (Native to UK Grid). Ultility service 220V single phase AC, 200A. Requires two non-standard current transformers (CT) YHCD SCT019 0-200A 33mA (http://www.yhdc.com/en/product/347/). Data sent from EmonTXv3 (q10 sec) via serial USB to the RaspberryPi 3 where front end processing is handeled in python (Power_Logger.py). 

Power Data Structure: `999(CT1) 999(CT2) 999(CT3) 999(CT4) 12099(Voltage) 0(Pulse Count)`

CT1 and CT2 are added together to get the total power usage in watts. 

All data is uploaded to Thingspeak.com (https://thingspeak.com/users/lantz) and EmonCMS.org (https://emoncms.org/)

#Install Notes
ABOVE REPO BUILT ON THE CONDITION THAT IT IS PLACED IN THE HOME DIRECTORY OF USER **PI** (`/home/pi/Power_Monitoring/`). Any deviation requires extensive editing of SH scripts and configuration files.

SVG_Processing.py **REQUIRES** `python-lxml`, `libxml2-dev` & `libxslt-dev`

```bash 
sudo apt-get install python-lxml
```

```bash
sudo apt-get install libxml2-dev libxslt-dev python-dev
```

`$LOCATION.location` keep file that represents *current* location. Sets the proper location varibles and paths for dropbox-uploader.

RaspberryPi 3 (NOOBS) does not allow ping to be run outside of SU. `network_restart.sh` placed in crontab bin folder and run as root.
```bash
sudo cp ./network_restart.sh /usr/local/bin/
```
Add the following to `/etc/crontab`:
```
*/5 * 	* * *	root	/usr/local/bin/network_restart.sh >> /var/log/network_restart.log 2>&1
```
Add the following to the *PI* user's crontab with `crontab -e` **OR** `./crontab_install.sh`
```
@reboot /home/pi/Power_Monitoring/Gateway_Logger.sh
@reboot /home/pi/Power_Monitoring/Power_Monitor.sh
@reboot /home/pi/Power_Monitoring/SVG_Processing.sh
@reboot /home/pi/Power_Monitoring/SVG_PNG_Script.sh
*/10 * * * * /home/pi/Power_Monitoring/tweeter.sh
*/15 * * * * /home/pi/Power_Monitoring/Dropbox-Uploader/data_log_update.sh
```
Pushing to Kindle requires `apache2`
