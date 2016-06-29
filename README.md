# Power_Monitoring
Homebrew home monitoring project. Includes multiple weather sensors and Open Power Monitoring EmonTX v3 sensor for power usage.

Weather sensors baised on Arduino Pro Mini (8mhz, 3.3v) with BME280 atmospheric sensor (Temp, Press, Humidity) and Hope RFM95x trancever. Tied with custom PCB. Blindly transmits data q96 sec with unique ID, above readings and a voltage read.

Above read by Arduino Pro Mini (8mhx, 3.3v) and Hope RFM95x transcever, transmitted to RaspberryPi 3 via USB serial connection where front end processing is handeled in the python scripts found here.
