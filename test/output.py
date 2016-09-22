import pandas as pd
import numpy as np
import time, datetime
import traceback
import sys, os.path
import requests
import codecs
import urllib2
import json

debug = False
verbose = False
request_timeout = 5

for arg in sys.argv:
	if arg == '-d':
		debug = True
		print("DEBUG IS ON")
	elif arg == '-v':
		verbose = True
		print("VERBOSE IS ON")
	elif arg == '-h':
		print("SVG_Processing.py script - LWH & NHH")
		print("Backend processing of data collected by Arduino based sensors for output to SVG/PNG file")
		print("Options:  [-d DEBUG] [-v VERBOSE] [-h HELP]")
		sys.exit()

if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
	location = 'dover'
	
	template_svg_filename = 'resources/DOVER_WX_TEMPLATE.svg'
	
	tides = False
	
	wuapi_update_freq = 200
	wunder_site_forcast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ma/cuttyhunk.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ma/cuttyhunk.json'
	
	sensor0      = '09'
	sensor0label = 'Outside'
	sensor1      = '08'
	sensor1label = 'Upstairs'
	sensor2      = '07'
	sensor2label = 'Downstairs'
	sensor3      = '05'
	sensor3label = 'Attic'
	sensor4      = '06'
	sensor4label = 'Garage'
	if debug:
		print(location)

elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
	location = 'cuttyhunk'
	
	tides = True
	tide_csv = 'https://tidesandcurrents.noaa.gov/noaatidepredictions/NOAATidesFacade.jsp?datatype=Annual+TXT&Stationid=8448376&text=datafiles%252F8448376%252F22092016%252F773%252F&imagename=images%2F8448376%2F22092016%2F773%2F8448376_2016-09-23.gif&bdate=20160922&timelength=daily&timeZone=2&dataUnits=1&interval=&edate=20160923&StationName=Cuttyhunk&Stationid_=8448376&state=MA&primary=Subordinate&datum=MLLW&timeUnits=2&ReferenceStationName=Newport&ReferenceStation=8452660&HeightOffsetLow=*0.93&HeightOffsetHigh=*+0.97&TimeOffsetLow=75&TimeOffsetHigh=80&pageview=dayly&print_download=true&Threshold=&thresholdvalue='
	
	template_svg_filename = 'resources/CUTTY_WX_TEMPLATE.svg'
	
	wuapi_update_freq = 50
	wunder_site_forcast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ny/carmel.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ny/carmel.json'
	
	sensor0      = '00'
	sensor0label = 'Outside'
	sensor1      = '01'
	sensor1label = 'Upstairs'
	sensor2      = '04'
	sensor2label = 'Reeds Room'
	sensor3      = None
	sensor3label = None
	sensor4      = None
	sensor4label = None
	if debug:
		print(location)

if (1):
	today = datetime.date.today()
	now = datetime.date.now()
	today_minus_one = datetime.date.today() + datetime.timedelta(days=-1)
	today_minus_two = datetime.date.today() + datetime.timedelta(days=-2)
	today_minus_three = datetime.date.today() + datetime.timedelta(days=-3)
	today_plus_one = datetime.date.today() + datetime.timedelta(days=1)
	today_plus_two = datetime.date.today() + datetime.timedelta(days=2)
	today_plus_three = datetime.date.today() + datetime.timedelta(days=3)

	forcastjson = requests.get(wunder_site_forcast_json, timeout=request_timeout)
	conditionjson = requests.get(wunder_site_conditions_json, timeout=request_timeout)
  
	if tides:
		tide_data = pd.read_table(tide_csv, sep='\t', skiprows=20, names = ["Date","Day","Time","Predict Feet","NULL1","Predict Cent","NULL2","High/Low"], dtype=str)
		tide_data['Datetime'] = pd.to_datetime(tide_data['Date'] + ' ' + tide_data['Time'])
		tide_data = tide_data.set_index('Datetime')
		tide_data = tide_data.drop(['Date','Time','Day','NULL1','NULL2','Predict Cent'],1)

		tide_today = tide_data[today.strftime("%Y-%m-%d")]
		tide_tomorrow = tide_data[tomorrow.strftime("%Y-%m-%d")]
