#! /bin/sh

cd /home/pi/Power_Monitoring

while :
do
	rsvg-convert -b white -o weather-script-output.png TEST.svg
	pngcrush -c 0 -ow weather-script-output.png
	/home/pi/Downloads/Dropbox-Uploader/dropbox_uploader.sh upload weather-script-output.png /Programing/
	/home/pi/Downloads/Dropbox-Uploader/dropbox_uploader.sh upload TEST.svg /Programing/
	sleep 20
done
