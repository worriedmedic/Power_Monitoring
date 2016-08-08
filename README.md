# Power_Monitoring
ABOVE REPO BUILT ON THE CONDITION THAT IT IS PLACED IN THE HOME DIRECTORY OF USER "PI" (/home/pi/Power_Monitoring/). Any deviation requires extensive editing of SH scripts and configuration files.

SVG_Processing.py REQUIRES "python-lxml", "libxml2-dev" & "libxslt-dev"
sudo apt-get install python-lxml
sudo apt-get install libxml2-dev libxslt-dev python-dev

Homebrew home monitoring project. Includes multiple weather sensors and Open Power Monitoring EmonTX v3 sensor for power usage.

Weather sensors baised on Arduino Pro Mini (8mhz, 3.3v) with BME280 atmospheric sensor (Temp, Press, Humidity) and Hope RFM95x trancever. Tied with custom PCB. Blindly transmits data q96 sec with unique ID, above readings and a voltage read.

Above read by Arduino Pro Mini (8mhx, 3.3v) and Hope RFM95x transcever, transmitted to RaspberryPi 3 via USB serial connection where front end processing is handeled in the python scripts found here.
