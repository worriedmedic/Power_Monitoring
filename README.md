#Power Monitoring
Homebrew home monitoring project. Includes multiple custom made weather sensors and Open Power Monitoring EmonTX v3 sensor for power usage.

Samelessly borrowing code from andreafabrizi Dropbox-Uploader (https://github.com/andreafabrizi/Dropbox-Uploader/), dweeber WiFi-Check (https://github.com/dweeber/WiFi_Check), thanks!

Weather sensors baised on Arduino Pro Mini (8mhz, 3.3v) with BME280 atmospheric sensor (Temp, Press, Humidity) and Hope RFM95x trancever, powered by x2 AA batteries. Blindly transmits data (q96 sec) with unique ID. Data packets are read by a Arduino Pro Mini (8mhx, 3.3v) and Hope RFM95x transcever, passed on to a RaspberryPi 3 (NOOBS) via USB serial connection where front end processing is handeled in python (Gateway_Logger.py). 

Weather Sensor Data Structure: `00(Address),T99.99(Temp-F),P1000.00(Pressure-hPa),H99.99(Humidity),V99.99(Voltage-%),099(RSSI)`
Sensors seem to stop transmitting when voltage reaches ~81%.

Open Power Monitoring EmonTXv3 modified for US use (Native to UK Grid). Ultility service 220V single phase AC, 200A. Requires two non-standard current transformers (CT) YHCD SCT019 0-200A 33mA (http://www.yhdc.com/en/product/347/). Data sent from EmonTXv3 (q10 sec) via serial USB to the RaspberryPi 3 where front end processing is handeled in python (Power_Logger.py). 

Power Data Structure: `999(CT1) 999(CT2) 999(CT3) 999(CT4) 12099(Voltage) 0(Pulse Count)`

CT1 and CT2 are added together to get the total power usage in watts. 

All data is uploaded to Thingspeak.com (https://thingspeak.com/users/lantz) and EmonCMS.org (https://emoncms.org/)

#Install Notes
ABOVE REPO BUILT ON THE CONDITION THAT IT IS PLACED IN THE HOME DIRECTORY OF USER **PI** (`/home/pi/Power_Monitoring/`). Any deviation requires extensive editing of SH scripts and configuration files. From the ~/ directory, run:
```
git clone http://github.com/worriedmedic/Power_Monitoring
```

`$LOCATION.location` keep file that represents *current* location and `rm` the file that does not. Sets the proper location varibles and paths for dropbox-uploader.

run `install_script.sh` found in `/home/pi/Power_Monitoring`

Will automatically install the following dependencies: `apache2`, `tightvncserver`, `fail2ban`, `ngrok`, `pngcrush`, `librsvg2-bin`, `python-lxml`, `libxml2-dev` & `libxslt-dev`. Will also install NGROK, copy the `network_restart.sh` to `/usr/local/bin/`, and add the necessary entries to the user's crontab. THE SCRIPT WILL NOT COMPLETELY SETUP *NGROK*, *DROPBOX_UPLOADER*, or the `/etc/crontab`.

VNC: https://www.raspberrypi.org/documentation/remote-access/vnc/

User Crontab:
```
@reboot /home/pi/Power_Monitoring/Gateway_Logger.sh
@reboot /home/pi/Power_Monitoring/Power_Monitor.sh
@reboot /home/pi/Power_Monitoring/SVG_PNG_Script.sh
@reboot python /home/pi/Power_Monitoring/Data_to_SVG.py >> /home/pi/Power_Monitoring/data_log/Data_to_SVG.log 2>&1
*/10 * * * * /home/pi/Power_Monitoring/tweeter.sh
*/15 * * * * /home/pi/Power_Monitoring/Dropbox-Uploader/data_log_update.sh
*/15 * * * * python /home/pi/Power_Monitoring/plotting/Matplotlib_plot.py >> /home/pi/Power_Monitoring/data_log/Matplotlib-plot.log 2>&1
*/15 * * * * /home/pi/Power_Monitoring/plotting/PNG_Processing.sh
```
`/etc/crontab`:
```
*/5 *   * * *   root    /usr/local/bin/network_restart.sh >> /var/log/network_restart.log 2>&1
@reboot		pi	ngrok start -all > /dev/null
```

Plotting Software Installed: `python-matplotlib`, `python-pandas`

http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20160918 09:00&end_date=20160918 23:59&station=8448376&product=water_level&datum=MWH&datum=MLW&units=english&time_zone=gmt&application=ports_screen&format=json
