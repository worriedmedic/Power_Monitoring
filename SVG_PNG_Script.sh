#! /bin/sh

cd /home/pi/Power_Monitoring

while :
do
	rsvg-convert -b white -o weather-script-output.png TEST.svg
	pngcrush -c 0 -ow weather-script-output.png
	sudo cp -f weather-script-output.png /var/www/html/weather-script-output.png
	sudo chmod 755 /var/www/html/weather-script-output.png
	sleep 10
done
