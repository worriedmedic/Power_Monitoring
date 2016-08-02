#! /bin/sh

cd "$(dirname "$0")"

while :
do
	rsvg-convert -b white -o /home/pi/Programing/Cuttyhunk_Wx_St/SVG_Kindle/weather-script-output.png /home/pi/Programing/Cuttyhunk_Wx_St/Data_Process/TEST.svg
	pngcrush -c 0 -ow weather-script-output.png
	sudo cp -f weather-script-output.png /var/www/html/weather-script-output.png
	sudo chmod 755 /var/www/html/weather-script-output.png
	sleep 10
done
