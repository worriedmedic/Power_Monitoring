#! /bin/sh
#Script converts SVG output to a PNG and then converts it properly so it can be displayed on the kindle
#Also copies the SVG and PNG file to dropbox

cd /home/pi/Power_Monitoring

while :
do
	rsvg-convert -b white -o weather-script-output.png TEST.svg
	pngcrush -c 0 -ow weather-script-output.png
	sudo cp -f weather-script-output.png /var/www/html/
	sudo chmod 755 /var/www/html/weather-script-output.png
	/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh upload weather-script-output.png /Programming/
	/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh upload TEST.svg /Programming/
	sleep 10
done
