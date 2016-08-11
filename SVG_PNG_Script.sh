#! /bin/sh
#Script converts SVG output to a PNG and then converts it properly so it can be displayed on the kindle
#Also copies the SVG and PNG file to dropbox

cd /home/pi/Power_Monitoring/output

while :
do
	rsvg-convert -b white -o weather-script-output.png weather-script-output.svg
	pngcrush -c 0 -ow weather-script-output.png
	sudo cp -f weather-script-output.png /var/www/html/
	sudo chmod 755 /var/www/html/weather-script-output.png
	if [ -f '/home/pi/Power_Monitoring/dover.location' ]; then
		/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh upload weather-script-output.png /Programming/dover/
		/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh upload weather-script-output.svg /Programming/dover/
	elif [ -f '/home/pi/Power_Monitoring/cuttyhunk.location' ]; then
		/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh upload weather-script-output.png /Programming/data_log/
		/home/pi/Power_Monitoring/Dropbox-Uploader/dropbox_uploader.sh upload weather-script-output.svg /Programming/data_log/
	fi

	sleep 10
done
