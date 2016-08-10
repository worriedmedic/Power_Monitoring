# Power_Monitoring
ABOVE REPO BUILT ON THE CONDITION THAT IT IS PLACED IN THE HOME DIRECTORY OF USER **PI** (/home/pi/Power_Monitoring/). Any deviation requires extensive editing of SH scripts and configuration files, and is generally not recommended.

Homebrew home monitoring project. Includes multiple custom made weather sensors and Open Power Monitoring EmonTX v3 sensor for power usage.

Weather sensors baised on Arduino Pro Mini (8mhz, 3.3v) with BME280 atmospheric sensor (Temp, Press, Humidity) and Hope RFM95x trancever. Blindly transmits data (q96 sec) with unique ID. Data packets are read by a Arduino Pro Mini (8mhx, 3.3v) and Hope RFM95x transcever, passed on to a RaspberryPi 3 (NOOBS) via USB serial connection where front end processing is handeled in python (Gateway_Logger.py). 

Weather Sensor Data Structure: 00(Address),T99.99(Temp-F),P1000.00(Pressure-hPa),H99.99(Humidity),V99.99(Voltage-%),099(RSSI)

Open Power Monitoring EmonTXv3 sends data (q10 sec) via serial USB to the RaspberryPi 3 where front end processing is handeled in python (Power_Logger.py).

#Install Notes
ABOVE REPO BUILT ON THE CONDITION THAT IT IS PLACED IN THE HOME DIRECTORY OF USER **PI** (/home/pi/Power_Monitoring/). Any deviation requires extensive editing of SH scripts and configuration files.

SVG_Processing.py REQUIRES "python-lxml", "libxml2-dev" & "libxslt-dev"

```bash 
sudo apt-get install python-lxml
```

```bash
sudo apt-get install libxml2-dev libxslt-dev python-dev
```

**$LOCATION.location** keep file that represents *current* location. Sets the proper location varibles and paths for dropbox-uploader.
