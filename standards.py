if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
	location = 'dover'
	today_minus_one = datetime.date.today() + datetime.timedelta(days=-1)
	today_plus_one = datetime.date.today() + datetime.timedelta(days=1)
	
	template_svg_filename = '/home/pi/Power_Monitoring/resources/DOVER_WX_TEMPLATE.svg'
	
	tide = False
	
	wunder_site_forecast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ny/carmel.json'
	wunder_site_astronomy_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/astronomy/q/ny/carmel.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ny/carmel.json'
	
	sensor0		= '09'
	sensor0label	= 'Outside'
	sensor1		= '08'
	sensor1label	= 'Upstairs'
	sensor2		= '07'
	sensor2label	= 'Master Bedroom'
	sensor3		= '05'
	sensor3label	= 'Guest Room'
	sensor4		= '06'
	sensor4label	= 'Garage'
	sensor5		= '04'
	sensor5label	= 'Downstairs'
	sensor6		= '03'
	sensor6label	= 'Laundry'
	sensor7		= '02'
	sensor7label	= 'Liam'
	if verbose:
		print(location)
	
elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
	location = 'cuttyhunk'
	today_minus_one = datetime.date.today() + datetime.timedelta(days=-1)
	today_plus_one = datetime.date.today() + datetime.timedelta(days=1)
	
	tide = True
	
	template_svg_filename = '/home/pi/Power_Monitoring/resources/CUTTY_WX_TEMPLATE.svg'
	
	wunder_site_forecast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ma/cuttyhunk.json'
	wunder_site_astronomy_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/astronomy/q/ma/cuttyhunk.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ma/cuttyhunk.json'
	
	sensor0		= '98'
	sensor0label	= 'Outside'
	sensor1		= '96'
	sensor1label	= 'Upstairs'
	sensor2		= '95'
	sensor2label	= 'Reeds Room'
	sensor3		= '97'
	sensor3label	= 'Barn'
	sensor4		= '99'
	sensor4label	= 'TEST'
	sensor5		= '88'
	sensor5label	= 'None'
	sensor6		= '87'
	sensor6label	= 'None'
	sensor7		= '86'
	sensor7label	= 'None'
	if verbose:
		print(location)
