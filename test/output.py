import pandas as pd
import numpy as np
import datetime, time
import traceback
import sys, os.path
import requests
import codecs
import urllib2
import json
import traceback
from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler

debug = False
verbose = False
request_timeout = 5
sensor_data = True
weather_data = True
global i
i = 0

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
	sensor3      = '06'
	sensor3label = 'Garage'
	sensor4      = '05'
	sensor4label = 'Attic'
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

def data_call():	
	today = datetime.date.today()
	now = datetime.datetime.now()
	today_minus_one = datetime.date.today() + datetime.timedelta(days=-1)
	today_minus_two = datetime.date.today() + datetime.timedelta(days=-2)
	today_minus_three = datetime.date.today() + datetime.timedelta(days=-3)
	today_plus_one = datetime.date.today() + datetime.timedelta(days=1)
	today_plus_two = datetime.date.today() + datetime.timedelta(days=2)
	today_plus_three = datetime.date.today() + datetime.timedelta(days=3)
	
	if tides:
		try:
			tide_data = pd.read_table(tide_csv, sep='\t', skiprows=20, names = ["Date","Day","Time","Predict Feet","NULL1","Predict Cent","NULL2","High/Low"], dtype=str)
			tide_data['Datetime'] = pd.to_datetime(tide_data['Date'] + ' ' + tide_data['Time'])
			tide_data = tide_data.set_index('Datetime')
			tide_data = tide_data.drop(['Date','Time','Day','NULL1','NULL2','Predict Cent'],1)
			tide_today = tide_data[today.strftime("%Y-%m-%d")]
			tide_tomorrow = tide_data[today_plus_one.strftime("%Y-%m-%d")]
			tide_yesterday = tide_data[today_minus_one.strftime("%Y-%m-%d")]
			if verbose:
				print("Tide Yesterday: ", tide_yesterday)
				print("Tide Today: ", tide_today)
				print("Tide Tomorrow: ", tide_tomorrow)
		except Exception:
			print("TIDES ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
				
	if weather_data:
		try:
			if i >= wuapi_update_freq or i == 0:
				global wind_mph, wind_gust, wind_direction, pressure_trend
				condition_data = pd.read_json(wunder_site_conditions_json, typ='series')
				forcast_data = pd.read_json(wunder_site_forcast_json, typ='series')
				wind_mph = condition_data.current_observation['wind_mph']
				wind_gust = condition_data.current_observation['wind_gust_mph']
				wind_direction = condition_data.current_observation['wind_dir']
				pressure_trend = condition_data.current_observation['pressure_trend']
				if verbose:
					print location, "Wind (MPH):", wind_mph, "Wind Gust (MPH):", wind_gust, "Wind Direction:", wind_direction, "Pressure Trend:", pressure_trend
		except Exception:
			print("WEATHER DATA ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
				
	if sensor_data:
		try:
			global data, data0, data1, data2, data3, data4
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
			data['Temperature'] = data['Temperature'].astype(float)
			data['Pressure'] = data['Pressure'].astype(float)
			data['Humidity'] = data['Humidity'].astype(float)
			data['Voltage'] = data['Voltage'].astype(float)
			data['RSSI'] = data['RSSI'].astype(float)
			data['Dewpoint'] = data['Temperature'].values - (0.36 * (100 - data['Humidity'].values))
			data0 = data.loc[data['Address'] == sensor0]
			data1 = data.loc[data['Address'] == sensor1]
			data2 = data.loc[data['Address'] == sensor2]
			data3 = data.loc[data['Address'] == sensor3]
			data4 = data.loc[data['Address'] == sensor4]
		except Exception:
			print("PANDAS ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
	
	try:
		if not data0.empty:
			global data0_global
			data0_global = {'time' 		: data0.index[-1:][0], 
				      'temperature'	: data0['Temperature'][-1:].values, 
				      'temperature_max'	: data0['Temperature'].max(),
				      'temperature_min' : data0['Temperature'].min(),
				      'pressure'	: data0['Pressure'][-1:].values,
				      'pressure_max'	: data0['Pressure'].max(),
				      'pressure_min'	: data0['Pressure'].min(),
				      'humidity'	: data0['Humidity'][-1:].values,
				      'humidity_max'	: data0['Humidity'].max(),
				      'humidity_min'	: data0['Humidity'].min(),
				      'dewpoint'	: data0['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data0['Dewpoint'].max(),
				      'dewpoint_min'	: data0['Dewpoint'].min(),
				      'voltage'		: data0['Voltage'][-1:].values,
				      'voltage_max'	: data0['Voltage'].max(),
				      'voltage_min'	: data0['Voltage'].min(),
				      'rssi'		: data0['RSSI'][-1:].values,
				      'rssi_max'	: data0['RSSI'].max(),
				      'rssi_min'	: data0['RSSI'].min()}
			
			if verbose:
				print sensor0label, "Time of Data Read:\t", data0_global['time']
				print sensor0label, "Temperature:\t", data0_global['temperature'], "H:", data0_global['temperature_max'], "L:", data0_global['temperature_min']
				print sensor0label, "Pressure:\t", data0_global['pressure'], "H:", data0_global['pressure_max'], "L:", data0_global['pressure_min']
				print sensor0label, "Humidity:\t", data0_global['humidity'], "H:", data0_global['humidity_max'], "L:", data0_global['humidity_min']
				print sensor0label, "Dewpoint:\t", data0_global['dewpoint'], "H:", data0_global['dewpoint_max'], "L:", data0_global['dewpoint_min']
				print sensor0label, "Voltage:\t\t", data0_global['voltage'], "H:", data0_global['voltage_max'], "L:", data0_global['voltage_min']
				print sensor0label, "RSSI:\t\t", data0_global['rssi'], "H:", data0_global['rssi_max'], "L:", data0_global['rssi_min']
	except Exception:
		print("DATA0 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data1.empty:
			global data1_global
			data1_global = {'time' 		: data1.index[-1:][0], 
				      'temperature'	: data1['Temperature'][-1:].values, 
				      'temperature_max'	: data1['Temperature'].max(),
				      'temperature_min' : data1['Temperature'].min(),
				      'pressure'	: data1['Pressure'][-1:].values,
				      'pressure_max'	: data1['Pressure'].max(),
				      'pressure_min'	: data1['Pressure'].min(),
				      'humidity'	: data1['Humidity'][-1:].values,
				      'humidity_max'	: data1['Humidity'].max(),
				      'humidity_min'	: data1['Humidity'].min(),
				      'dewpoint'	: data1['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data1['Dewpoint'].max(),
				      'dewpoint_min'	: data1['Dewpoint'].min(),
				      'voltage'		: data1['Voltage'][-1:].values,
				      'voltage_max'	: data1['Voltage'].max(),
				      'voltage_min'	: data1['Voltage'].min(),
				      'rssi'		: data1['RSSI'][-1:].values,
				      'rssi_max'	: data1['RSSI'].max(),
				      'rssi_min'	: data1['RSSI'].min()}
			
			if verbose:
				print sensor1label, "Time of Data Read:\t", data1_global['time']
				print sensor1label, "Temperature:\t", data1_global['temperature'], "H:", data1_global['temperature_max'], "L:", data1_global['temperature_min']
				print sensor1label, "Pressure:\t", data1_global['pressure'], "H:", data1_global['pressure_max'], "L:", data1_global['pressure_min']
				print sensor1label, "Humidity:\t", data1_global['humidity'], "H:", data1_global['humidity_max'], "L:", data1_global['humidity_min']
				print sensor1label, "Dewpoint:\t", data1_global['dewpoint'], "H:", data1_global['dewpoint_max'], "L:", data1_global['dewpoint_min']
				print sensor1label, "Voltage:\t\t", data1_global['voltage'], "H:", data1_global['voltage_max'], "L:", data1_global['voltage_min']
				print sensor1label, "RSSI:\t\t", data1_global['rssi'], "H:", data1_global['rssi_max'], "L:", data1_global['rssi_min']
	except Exception:
		print("DATA1 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data2.empty:
			global data2_global
			data2_global = {'time' 		: data2.index[-1:][0], 
				      'temperature'	: data2['Temperature'][-1:].values, 
				      'temperature_max'	: data2['Temperature'].max(),
				      'temperature_min' : data2['Temperature'].min(),
				      'pressure'	: data2['Pressure'][-1:].values,
				      'pressure_max'	: data2['Pressure'].max(),
				      'pressure_min'	: data2['Pressure'].min(),
				      'humidity'	: data2['Humidity'][-1:].values,
				      'humidity_max'	: data2['Humidity'].max(),
				      'humidity_min'	: data2['Humidity'].min(),
				      'dewpoint'	: data2['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data2['Dewpoint'].max(),
				      'dewpoint_min'	: data2['Dewpoint'].min(),
				      'voltage'		: data2['Voltage'][-1:].values,
				      'voltage_max'	: data2['Voltage'].max(),
				      'voltage_min'	: data2['Voltage'].min(),
				      'rssi'		: data2['RSSI'][-1:].values,
				      'rssi_max'	: data2['RSSI'].max(),
				      'rssi_min'	: data2['RSSI'].min()}
			
			if verbose:
				print sensor2label, "Time of Data Read:\t", data2_global['time']
				print sensor2label, "Temperature:\t", data2_global['temperature'], "H:", data2_global['temperature_max'], "L:", data2_global['temperature_min']
				print sensor2label, "Pressure:\t", data2_global['pressure'], "H:", data2_global['pressure_max'], "L:", data2_global['pressure_min']
				print sensor2label, "Humidity:\t", data2_global['humidity'], "H:", data2_global['humidity_max'], "L:", data2_global['humidity_min']
				print sensor2label, "Dewpoint:\t", data2_global['dewpoint'], "H:", data2_global['dewpoint_max'], "L:", data2_global['dewpoint_min']
				print sensor2label, "Voltage:\t\t", data2_global['voltage'], "H:", data2_global['voltage_max'], "L:", data2_global['voltage_min']
				print sensor2label, "RSSI:\t\t", data2_global['rssi'], "H:", data2_global['rssi_max'], "L:", data2_global['rssi_min']
	except Exception:
		print("DATA2 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data3.empty:
			global data3_global
			data3_global = {'time' 		: data3.index[-1:][0], 
				      'temperature'	: data3['Temperature'][-1:].values, 
				      'temperature_max'	: data3['Temperature'].max(),
				      'temperature_min' : data3['Temperature'].min(),
				      'pressure'	: data3['Pressure'][-1:].values,
				      'pressure_max'	: data3['Pressure'].max(),
				      'pressure_min'	: data3['Pressure'].min(),
				      'humidity'	: data3['Humidity'][-1:].values,
				      'humidity_max'	: data3['Humidity'].max(),
				      'humidity_min'	: data3['Humidity'].min(),
				      'dewpoint'	: data3['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data3['Dewpoint'].max(),
				      'dewpoint_min'	: data3['Dewpoint'].min(),
				      'voltage'		: data3['Voltage'][-1:].values,
				      'voltage_max'	: data3['Voltage'].max(),
				      'voltage_min'	: data3['Voltage'].min(),
				      'rssi'		: data3['RSSI'][-1:].values,
				      'rssi_max'	: data3['RSSI'].max(),
				      'rssi_min'	: data3['RSSI'].min()}
			
			if verbose:
				print sensor3label, "Time of Data Read:\t", data3_global['time']
				print sensor3label, "Temperature:\t", data3_global['temperature'], "H:", data3_global['temperature_max'], "L:", data3_global['temperature_min']
				print sensor3label, "Pressure:\t", data3_global['pressure'], "H:", data3_global['pressure_max'], "L:", data3_global['pressure_min']
				print sensor3label, "Humidity:\t", data3_global['humidity'], "H:", data3_global['humidity_max'], "L:", data3_global['humidity_min']
				print sensor3label, "Dewpoint:\t", data3_global['dewpoint'], "H:", data3_global['dewpoint_max'], "L:", data3_global['dewpoint_min']
				print sensor3label, "Voltage:\t\t", data3_global['voltage'], "H:", data3_global['voltage_max'], "L:", data3_global['voltage_min']
				print sensor3label, "RSSI:\t\t", data3_global['rssi'], "H:", data3_global['rssi_max'], "L:", data3_global['rssi_min']
	except Exception:
		print("DATA3 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data4.empty:
			global data4_global
			data4_global = {'time' 		: data4.index[-1:][0], 
				      'temperature'	: data4['Temperature'][-1:].values, 
				      'temperature_max'	: data4['Temperature'].max(),
				      'temperature_min' : data4['Temperature'].min(),
				      'pressure'	: data4['Pressure'][-1:].values,
				      'pressure_max'	: data4['Pressure'].max(),
				      'pressure_min'	: data4['Pressure'].min(),
				      'humidity'	: data4['Humidity'][-1:].values,
				      'humidity_max'	: data4['Humidity'].max(),
				      'humidity_min'	: data4['Humidity'].min(),
				      'dewpoint'	: data4['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data4['Dewpoint'].max(),
				      'dewpoint_min'	: data4['Dewpoint'].min(),
				      'voltage'		: data4['Voltage'][-1:].values,
				      'voltage_max'	: data4['Voltage'].max(),
				      'voltage_min'	: data4['Voltage'].min(),
				      'rssi'		: data4['RSSI'][-1:].values,
				      'rssi_max'	: data4['RSSI'].max(),
				      'rssi_min'	: data4['RSSI'].min()}
			
			if verbose:
				print sensor4label, "Time of Data Read:\t", data4_global['time']
				print sensor4label, "Temperature:\t", data4_global['temperature'], "H:", data4_global['temperature_max'], "L:", data4_global['temperature_min']
				print sensor4label, "Pressure:\t", data4_global['pressure'], "H:", data4_global['pressure_max'], "L:", data4_global['pressure_min']
				print sensor4label, "Humidity:\t", data4_global['humidity'], "H:", data4_global['humidity_max'], "L:", data4_global['humidity_min']
				print sensor4label, "Dewpoint:\t", data4_global['dewpoint'], "H:", data4_global['dewpoint_max'], "L:", data4_global['dewpoint_min']
				print sensor4label, "Voltage:\t\t", data4_global['voltage'], "H:", data4_global['voltage_max'], "L:", data4_global['voltage_min']
				print sensor4label, "RSSI:\t\t", data4_global['rssi'], "H:", data4_global['rssi_max'], "L:", data4_global['rssi_min']
	except Exception:
			print("DATA4 ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)

def element_upd_80(x):
	for element in tree.iter():
		if element.tag.split("}")[1] == "path":
			if element.get("id") == "b%sBat4" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat3" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat2" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat1" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat0" %x:
				element.attrib['class'] = ''

def element_upd_85(x):
	for element in tree.iter():
		if element.tag.split("}")[1] == "path":
			if element.get("id") == "b%sBat4" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat3" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat2" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat1" %x:
				element.attrib['class'] = ''
			if element.get("id") == "b%sBat0" %x:
				element.attrib['class'] = 'st3'

def element_upd_90(x):
	for element in tree.iter():
		if element.tag.split("}")[1] == "path":
			if element.get("id") == "b%sBat4" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat3" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat2" %x:
				element.attrib['class'] = ''
			if element.get("id") == "b%sBat1" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat0" %x:
				element.attrib['class'] = 'st3'

def element_upd_95(x):
	for element in tree.iter():
		if element.tag.split("}")[1] == "path":
			if element.get("id") == "b%sBat4" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat3" %x:
				element.attrib['class'] = ''
			if element.get("id") == "b%sBat2" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat1" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat0" %x:
				element.attrib['class'] = 'st3'

def element_upd_100(x):
	for element in tree.iter():
		if element.tag.split("}")[1] == "path":
			if element.get("id") == "b%sBat4" %x:
				element.attrib['class'] = ''
			if element.get("id") == "b%sBat3" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat2" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat1" %x:
				element.attrib['class'] = 'st3'
			if element.get("id") == "b%sBat0" %x:
				element.attrib['class'] = 'st3'

def battery_update(bat, dataglobal, datalabel):
	if (0 <= dataglobal['voltage'] < 80):
		element_upd_80(bat)
		if verbose:
			print(datalabel, dataglobal['voltage'], " - 0 to 80")
	elif (80 <= dataglobal['voltage'] < 85): 
		element_upd_85(bat)
		if verbose:
			print(datalabel, dataglobal['voltage'], " - 80 to 85")
	elif (85 <= dataglobal['voltage'] < 90):
		element_upd_90(bat)
		if verbose:
			print(datalabel, dataglobal['voltage'], " - 85 to 90")
	elif (90 <= dataglobal['voltage'] < 95):
		element_upd_95(bat)
		if verbose:
			print(datalabel, dataglobal['voltage'], " - 90 to 95")
	elif (95 <= dataglobal['voltage']):
		element_upd_100(bat)
		if verbose:
			print(datalabel, dataglobal['voltage'], " - 95 to 100")

def svg_update():
	today = datetime.date.today()
	now = datetime.datetime.now()
	try:
		global tree
		tree = etree.parse(open(template_svg_filename, 'r'))
		battery_update('00', data0_global, sensor0label)
		battery_update('01', data1_global, sensor1label)
		battery_update('02', data2_global, sensor2label)
		battery_update('03', data3_global, sensor3label)
		battery_update('04', data4_global, sensor4label)
		tree.write('output/weather-script-output1.svg')
	except Exception:
		print("BATTERY TO SVG ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		tree = etree.parse(open('output/weather-script-output1.svg', 'r'))
		if pressure_trend in ['+']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "ple":
						element.attrib['class'] = 'st3'
					if element.get("id") == "pup":
						element.attrib['class'] = ''
					if element.get("id") == "pdn":
						element.attrib['class'] = 'st3'
			if verbose:
				print "Pressure Up"
		
		elif pressure_trend in ['0']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "ple":
						element.attrib['class'] = ''
					if element.get("id") == "pup":
						element.attrib['class'] = 'st3'
					if element.get("id") == "pdn":
						element.attrib['class'] = 'st3'
			if verbose:
				print "Pressure Neutral"
		
		elif pressure_trend in ['-']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "ple":
						element.attrib['class'] = 'st3'
					if element.get("id") == "pup":
						element.attrib['class'] = 'st3'
					if element.get("id") == "pdn":
						element.attrib['class'] = ''
			if verbose:
				print "Pressure Down"
		
		tree.write('output/weather-script-output1.svg')
	
	except Exception:
		print("PRESSURE TO SVG ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		tree = etree.parse(open('output/weather-script-output1.svg', 'r'))
		if wind_direction in ['NNW', 'N', 'NNE', 'North']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "NORTH")
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['NE']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "NORTH EAST")
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['ENE', 'E', 'ESE', 'East']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "EAST")
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['SE']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "SOUTH EAST")
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['SSE', 'S', 'SSW', 'South']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "SOUTH")
					elif element.get("id") == "wdsw":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['SW']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "SOUTH WEST")
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['WSW', 'W', 'WNW', 'West']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "WEST")
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = 'st3'
		elif wind_direction in ['NW']:
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "wdno":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdne":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdea":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdse":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdso":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdsw":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdwe":
						element.attrib['class'] = 'st3'
					elif element.get("id") == "wdnw":
						element.attrib['class'] = ''
						if verbose:
							print(wind_direction, "NORTH WEST")
		tree.write('output/weather-script-output1.svg')
		
	except Exception:
		print("WIND_DIR TO SVG ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	try:
		output = codecs.open('output/weather-script-output1.svg', 'r', encoding='utf-8').read()
		output = output.replace('CURDATE', today.strftime("%m/%d/%Y"))
		output = output.replace('CURTIME', now.strftime("%H:%m"))
		#output = output.replace('SNRISE', sun_rise)
		#output = output.replace('SNSET', sun_down)
		#output = output.replace('FORHI', str(exp_hi))
		#output = output.replace('FORLO', str(exp_lo))
		output = output.replace('WSP', str(wind_mph))
		output = output.replace('WGUS', str(wind_gust))
		if data0_global['temperature'] >= 100:
			output = output.replace('TMPE', "{0:.1f}".format(float(data0_global['temperature'])))
		elif data0_global['temperature'] < 100:
			output = output.replace('TMPE', "{0:.2f}".format(float(data0_global['temperature'])))
		if data1_global['temperature'] >= 100:
			output = output.replace('TMPI', "{0:.1f}".format(float(data1_global['temperature'])))
		elif data1_global['temperature'] < 100:
			output = output.replace('TMPI', "{0:.2f}".format(float(data1_global['temperature'])))
		if data2_global['temperature'] >= 100:
			output = output.replace('TMPG', "{0:.1f}".format(float(data2_global['temperature'])))
		elif data2_global['temperature'] < 100:
			output = output.replace('TMPG', "{0:.2f}".format(float(data2_global['temperature'])))
		if data3_global['temperature'] >= 100:
			output = output.replace('TMPD', "{0:.1f}".format(float(data3_global['temperature'])))
		elif data3_global['temperature'] < 100:
			output = output.replace('TMPD', "{0:.2f}".format(float(data3_global['temperature'])))
		if data0_global['pressure'] >= 1000:
			output = output.replace('PRESS', "{0:.0f}".format(float(data0_global['pressure'])))
		elif data0_global['pressure'] < 1000:
			output = output.replace('PRESS', "{0:.1f}".format(float(data0_global['pressure'])))
		
		output = output.replace('RLHUM', "{0:.2f}".format(float(data0_global['humidity'])))
		output = output.replace('DWPNT', "{0:.2f}".format(float(data0_global['dewpoint'])))
		#output = output.replace('TDNTY', str(tide_pre_type))
		#output = output.replace('TDNTM', old.strftime('%H:%M'))
		#output = output.replace('TDNLV', str(tide_pre_mag))
		#output = output.replace('TDFTY', str(tide_next_type))
		#output = output.replace('TDFTM', tide_datetime.strftime('%H:%M'))
		#output = output.replace('TDFLV', str(tide_next_mag))
		codecs.open('output/weather-script-output1.svg', 'w', encoding='utf-8').write(output)
		
	except Exception:
		print("CODECS TO SVG ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

if(1):
	scheduler = BlockingScheduler()
	scheduler.add_job(data_call, 'interval', seconds=60)
	scheduler.add_job(svg_update, 'interval', seconds=60)
	
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
