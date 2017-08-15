import sys, os.path

if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
	######## GLOBAL VARS ########
	location = 'dover'
	sensor0		= 9
	sensor0label	= 'Outside'
	sensor1		= 8
	sensor1label	= 'Upstairs'
	sensor2		= 7
	sensor2label	= 'Master Bedroom'
	sensor3		= 5
	sensor3label	= 'Guest Room'
	sensor4		= 6
	sensor4label	= 'Garage'
	sensor5		= 4
	sensor5label	= 'Downstairs'
	sensor6		= 3
	sensor6label	= 'Laundry'
	sensor7		= 2
	sensor7label	= 'Liam'
	######## GATEWAY VARS ########
	gateway_addr = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A104VAFG-if00-port0'
	######## DATA VARS ########
	template_svg_filename = '/home/pi/Power_Monitoring/resources/DOVER_WX_TEMPLATE.svg'
	tide = False
	wunder_site_forecast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ny/carmel.json'
	wunder_site_astronomy_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/astronomy/q/ny/carmel.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ny/carmel.json'
	######## PLOTTING VARS ########
	td           = '48H'
	plt_size_x   = 10
	plt_size_y   = 8
	plt_size_dpi = 100
	plot_style   = 'bmh'
elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
	######## GLOBAL VARS ########
	location = 'cuttyhunk'
	sensor0		= 98
	sensor0label	= 'Outside'
	sensor1		= 96
	sensor1label	= 'Upstairs'
	sensor2		= 95
	sensor2label	= 'Reeds Room'
	sensor3		= 97
	sensor3label	= 'Barn'
	sensor4		= 99
	sensor4label	= 'TEST'
	sensor5		= 88
	sensor5label	= 'None'
	sensor6		= 87
	sensor6label	= 'None'
	sensor7		= 86
	sensor7label	= 'None'
	######## GATEWAY VARS ########
	gateway_addr = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AL02CC7C-if00-port0'
	######## DATA VARS ########
	tide = True
	template_svg_filename = '/home/pi/Power_Monitoring/resources/CUTTY_WX_TEMPLATE.svg'
	wunder_site_forecast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ma/cuttyhunk.json'
	wunder_site_astronomy_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/astronomy/q/ma/cuttyhunk.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ma/cuttyhunk.json'
	######## PLOTTING VARS ########
	td           = '72H'
	plt_size_x   = 10
	plt_size_y   = 8
	plt_size_dpi = 100
	plot_style   = 'bmh'
