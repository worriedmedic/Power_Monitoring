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
sensor_data = True
weather_data = True

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
	now = datetime.datetime.now()
	today_minus_one = datetime.date.today() + datetime.timedelta(days=-1)
	today_minus_two = datetime.date.today() + datetime.timedelta(days=-2)
	today_minus_three = datetime.date.today() + datetime.timedelta(days=-3)
	today_plus_one = datetime.date.today() + datetime.timedelta(days=1)
	today_plus_two = datetime.date.today() + datetime.timedelta(days=2)
	today_plus_three = datetime.date.today() + datetime.timedelta(days=3)
	if tides:
		tide_data = pd.read_table(tide_csv, sep='\t', skiprows=20, names = ["Date","Day","Time","Predict Feet","NULL1","Predict Cent","NULL2","High/Low"], dtype=str)
		tide_data['Datetime'] = pd.to_datetime(tide_data['Date'] + ' ' + tide_data['Time'])
		tide_data = tide_data.set_index('Datetime')
		tide_data = tide_data.drop(['Date','Time','Day','NULL1','NULL2','Predict Cent'],1)
		tide_today = tide_data[today.strftime("%Y-%m-%d")]
		tide_tomorrow = tide_data[today_plus_one.strftime("%Y-%m-%d")]
		tide_yesterday = tide_data[today_minus_one.strftime("%Y-%m-%d")]
		print("Tide Yesterday: ", tide_yesterday)
		print("Tide Today: ", tide_today)
		print("Tide Tomorrow: ", tide_tomorrow)
	if weather_data:
		condition_data = pd.read_json(wunder_site_conditions_json, typ='series')
		forcast_data = pd.read_json(wunder_site_forcast_json, typ='series')
		
	if sensor_data:
		data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today_minus_one.strftime("%Y-%m") + '/' + str(today_minus_one) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today_minus_two.strftime("%Y-%m") + '/' + str(today_minus_two) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data = pd.concat([data_2prior, data_yest, data_today])
		data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
		data = data.drop(['Date', 'Time'], 1)
		data = data.set_index('Datetime')
		data['Temperature'] = data['Temperature'].str.replace('T', '')
		data['Pressure'] = data['Pressure'].str.replace('P', '')
		data['Humidity'] = data['Humidity'].str.replace('H', '')
		data['Voltage'] = data['Voltage'].str.replace('V', '')
		data0 = data.loc[data['Address'] == sensor0]
		data1 = data.loc[data['Address'] == sensor1]
		data2 = data.loc[data['Address'] == sensor2]
		data3 = data.loc[data['Address'] == sensor3]
		data4 = data.loc[data['Address'] == sensor4]
		
		if not data0.empty:
			data0_readtime = data0.index[-1:][0]
			data0_temperature = data0['Temperature'][-1:].values
			print sensor0label, "Time of Data Read: ", data0_readtime
			print sensor0label, "Temperature: ", data0_temperature
			print sensor0label, "Pressure: ", data0['Pressure'][-1:].values
			print sensor0label, "Humidity: ", data0['Humidity'][-1:].values
			print sensor0label, "Voltage: ", data0['Voltage'][-1:].values
			print sensor0label, "RSSI: ", data0['RSSI'][-1:].values
		
		if not data1.empty:
			print sensor1label, "Time of Data Read: ", data1.index[-1:][0]
			print sensor1label, "Temperature: ", data1['Temperature'][-1:].values
			print sensor1label, "Pressure: ", data1['Pressure'][-1:].values
			print sensor1label, "Humidity: ", data1['Humidity'][-1:].values
			print sensor1label, "Voltage: ", data1['Voltage'][-1:].values
			print sensor1label, "RSSI: ", data1['RSSI'][-1:].values
		
		if not data2.empty:
			print sensor2label, "Time of Data Read: ", data2.index[-1:][0]
			print sensor2label, "Temperature: ", data2['Temperature'][-1:].values
			print sensor2label, "Pressure: ", data2['Pressure'][-1:].values
			print sensor2label, "Humidity: ", data2['Humidity'][-1:].values
			print sensor2label, "Voltage: ", data2['Voltage'][-1:].values
			print sensor2label, "RSSI: ", data2['RSSI'][-1:].values
		
		if not data3.empty:
			print sensor3label, "Time of Data Read: ", data3.index[-1:][0]
			print sensor3label, "Temperature: ", data3['Temperature'][-1:].values
			print sensor3label, "Pressure: ", data3['Pressure'][-1:].values
			print sensor3label, "Humidity: ", data3['Humidity'][-1:].values
			print sensor3label, "Voltage: ", data3['Voltage'][-1:].values
			print sensor3label, "RSSI: ", data3['RSSI'][-1:].values
		
		if not data4.empty:
			print sensor4label, "Time of Data Read: ", data4.index[-1:][0]
			print sensor4label, "Temperature: ", data4['Temperature'][-1:].values
			print sensor4label, "Pressure: ", data4['Pressure'][-1:].values
			print sensor4label, "Humidity: ", data4['Humidity'][-1:].values
			print sensor4label, "Voltage: ", data4['Voltage'][-1:].values
			print sensor4label, "RSSI: ", data4['RSSI'][-1:].values
