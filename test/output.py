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
from apscheduler.schedulers.blocking import BackgroundScheduler

debug = False
verbose = False
request_timeout = 5
sensor_data = True
weather_data = True
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
	global data, data0, data1, data2, data3, data4
	
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
			global data0_readtime, data0_temperature, data0_temperature_max, data0_temperature_min, data0_pressure, data0_pressure_max, data0_pressure_min, data0_humidity, data0_humidity_max, data0_humidity_min, data0_dewpoint, data0_dewpoint_max, data0_dewpoint_min, data0_voltage, data0_voltage_max, data0_voltage_min, data0_rssi, data0_rssi_max, data0_rssi_min
			data0_readtime = data0.index[-1:][0]
			data0_temperature = data0['Temperature'][-1:].values
			data0_temperature_max = data0['Temperature'].max()
			data0_temperature_min = data0['Temperature'].min()
			data0_pressure = data0['Pressure'][-1:].values
			data0_pressure_max = data0['Pressure'].max()
			data0_pressure_min = data0['Pressure'].min()
			data0_humidity = data0['Humidity'][-1:].values
			data0_humidity_max = data0['Humidity'].max()
			data0_humidity_min = data0['Humidity'].min()
			data0_dewpoint = data0['Dewpoint'][-1:].values
			data0_dewpoint_max = data3['Dewpoint'].max()
			data0_dewpoint_min = data3['Dewpoint'].min()
			data0_voltage = data0['Voltage'][-1:].values
			data0_voltage_max = data0['Voltage'].max()
			data0_voltage_min = data0['Voltage'].min()
			data0_rssi = data0['RSSI'][-1:].values
			data0_rssi_max = data0['RSSI'].max()
			data0_rssi_min = data0['RSSI'].min()
			if verbose:
				print sensor0label, "Time of Data Read:\t", data0_readtime
				print sensor0label, "Temperature:\t", data0_temperature, "H:", data0_temperature_max, "L:", data0_temperature_min
				print sensor0label, "Pressure:\t", data0_pressure, "H:", data0_pressure_max, "L:", data0_pressure_min
				print sensor0label, "Humidity:\t", data0_humidity, "H:", data0_humidity_max, "L:", data0_humidity_min
				print sensor0label, "Dewpoint:\t", data0_dewpoint, "H:", data0_dewpoint_max, "L:", data0_dewpoint_min
				print sensor0label, "Voltage:\t\t", data0_voltage, "H:", data0_voltage_max, "L:", data0_voltage_min
				print sensor0label, "RSSI:\t\t", data0_rssi, "H:", data0_rssi_max, "L:", data0_rssi_min
	except Exception:
		print("DATA0 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data1.empty:
			global data1_readtime, data1_temperature, data1_temperature_max, data1_temperature_min, data1_pressure, data1_pressure_max, data1_pressure_min, data1_humidity, data1_humidity_max, data1_humidity_min, data1_dewpoint, data1_dewpoint_max, data1_dewpoint_min, data1_voltage, data1_voltage_max, data1_voltage_min, data1_rssi, data1_rssi_max, data1_rssi_min
			data1_readtime = data1.index[-1:][0]
			data1_temperature = data1['Temperature'][-1:].values
			data1_temperature_max = data1['Temperature'].max()
			data1_temperature_min = data1['Temperature'].min()
			data1_pressure = data1['Pressure'][-1:].values
			data1_pressure_max = data1['Pressure'].max()
			data1_pressure_min = data1['Pressure'].min()
			data1_humidity = data1['Humidity'][-1:].values
			data1_humidity_max = data1['Humidity'].max()
			data1_humidity_min = data1['Humidity'].min()
			data1_dewpoint = data1['Dewpoint'][-1:].values
			data1_dewpoint_max = data3['Dewpoint'].max()
			data1_dewpoint_min = data3['Dewpoint'].min()
			data1_voltage = data1['Voltage'][-1:].values
			data1_voltage_max = data1['Voltage'].max()
			data1_voltage_min = data1['Voltage'].min()
			data1_rssi = data1['RSSI'][-1:].values
			data1_rssi_max = data1['RSSI'].max()
			data1_rssi_min = data1['RSSI'].min()
			if verbose:
				print sensor1label, "Time of Data Read:\t", data1_readtime
				print sensor1label, "Temperature:\t", data1_temperature, "H:", data1_temperature_max, "L:", data1_temperature_min
				print sensor1label, "Pressure:\t", data1_pressure, "H:", data1_pressure_max, "L:", data1_pressure_min
				print sensor1label, "Humidity:\t", data1_humidity, "H:", data1_humidity_max, "L:", data1_humidity_min
				print sensor1label, "Dewpoint:\t", data1_dewpoint, "H:", data1_dewpoint_max, "L:", data1_dewpoint_min
				print sensor1label, "Voltage:\t\t", data1_voltage, "H:", data1_voltage_max, "L:", data1_voltage_min
				print sensor1label, "RSSI:\t\t", data1_rssi, "H:", data1_rssi_max, "L:", data1_rssi_min
	except Exception:
		print("DATA1 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data2.empty:
			global data2_readtime, data2_temperature, data2_temperature_max, data2_temperature_min, data2_pressure, data2_pressure_max, data2_pressure_min, data2_humidity, data2_humidity_max, data2_humidity_min, data2_dewpoint, data2_dewpoint_max, data2_dewpoint_min, data2_voltage, data2_voltage_max, data2_voltage_min, data2_rssi, data2_rssi_max, data2_rssi_min
			data2_readtime = data2.index[-1:][0]
			data2_temperature = data2['Temperature'][-1:].values
			data2_temperature_max = data2['Temperature'].max()
			data2_temperature_min = data2['Temperature'].min()
			data2_pressure = data2['Pressure'][-1:].values
			data2_pressure_max = data2['Pressure'].max()
			data2_pressure_min = data2['Pressure'].min()
			data2_humidity = data2['Humidity'][-1:].values
			data2_humidity_max = data2['Humidity'].max()
			data2_humidity_min = data2['Humidity'].min()
			data2_dewpoint = data2['Dewpoint'][-1:].values
			data2_dewpoint_max = data3['Dewpoint'].max()
			data2_dewpoint_min = data3['Dewpoint'].min()
			data2_voltage = data2['Voltage'][-1:].values
			data2_voltage_max = data2['Voltage'].max()
			data2_voltage_min = data2['Voltage'].min()
			data2_rssi = data2['RSSI'][-1:].values
			data2_rssi_max = data2['RSSI'].max()
			data2_rssi_min = data2['RSSI'].min()
			if verbose:
				print sensor2label, "Time of Data Read:\t", data2_readtime
				print sensor2label, "Temperature:\t", data2_temperature, "H:", data2_temperature_max, "L:", data2_temperature_min
				print sensor2label, "Pressure:\t", data2_pressure, "H:", data2_pressure_max, "L:", data2_pressure_min
				print sensor2label, "Humidity:\t", data2_humidity, "H:", data2_humidity_max, "L:", data2_humidity_min
				print sensor2label, "Dewpoint:\t", data2_dewpoint, "H:", data2_dewpoint_max, "L:", data2_dewpoint_min
				print sensor2label, "Voltage:\t\t", data2_voltage, "H:", data2_voltage_max, "L:", data2_voltage_min
				print sensor2label, "RSSI:\t\t", data2_rssi, "H:", data2_rssi_max, "L:", data2_rssi_min
	except Exception:
		print("DATA2 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data3.empty:
			global data3_readtime, data3_temperature, data3_temperature_max, data3_temperature_min, data3_pressure, data3_pressure_max, data3_pressure_min, data3_humidity, data3_humidity_max, data3_humidity_min, data3_dewpoint, data3_dewpoint_max, data3_dewpoint_min, data3_voltage, data3_voltage_max, data3_voltage_min, data3_rssi, data3_rssi_max, data3_rssi_min
			data3_readtime = data3.index[-1:][0]
			data3_temperature = data3['Temperature'][-1:].values
			data3_temperature_max = data3['Temperature'].max()
			data3_temperature_min = data3['Temperature'].min()
			data3_pressure = data3['Pressure'][-1:].values
			data3_pressure_max = data3['Pressure'].max()
			data3_pressure_min = data3['Pressure'].min()
			data3_humidity = data3['Humidity'][-1:].values
			data3_humidity_max = data3['Humidity'].max()
			data3_humidity_min = data3['Humidity'].min()
			data3_dewpoint = data3['Dewpoint'][-1:].values
			data3_dewpoint_max = data3['Dewpoint'].max()
			data3_dewpoint_min = data3['Dewpoint'].min()
			data3_voltage = data3['Voltage'][-1:].values
			data3_voltage_max = data3['Voltage'].max()
			data3_voltage_min = data3['Voltage'].min()
			data3_rssi = data3['RSSI'][-1:].values
			data3_rssi_max = data3['RSSI'].max()
			data3_rssi_min = data3['RSSI'].min()
			if verbose:
				print sensor3label, "Time of Data Read:\t", data3_readtime
				print sensor3label, "Temperature:\t", data3_temperature, "H:", data3_temperature_max, "L:", data3_temperature_min
				print sensor3label, "Pressure:\t", data3_pressure, "H:", data3_pressure_max, "L:", data3_pressure_min
				print sensor3label, "Humidity:\t", data3_humidity, "H:", data3_humidity_max, "L:", data3_humidity_min
				print sensor3label, "Dewpoint:\t", data3_dewpoint, "H:", data3_dewpoint_max, "L:", data3_dewpoint_min
				print sensor3label, "Voltage:\t\t", data3_voltage, "H:", data3_voltage_max, "L:", data3_voltage_min
				print sensor3label, "RSSI:\t\t", data3_rssi, "H:", data3_rssi_max, "L:", data3_rssi_min
	except Exception:
		print("DATA3 ERROR", today, now)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
	
	try:
		if not data4.empty:
			global data4_readtime, data4_temperature, data4_temperature_max, data4_temperature_min, data4_pressure, data4_pressure_max, data4_pressure_min, data4_humidity, data4_humidity_max, data4_humidity_min, data4_dewpoint, data4_dewpoint_max, data4_dewpoint_min, data4_voltage, data4_voltage_max, data4_voltage_min, data4_rssi, data4_rssi_max, data4_rssi_min
			data4_readtime = data4.index[-1:][0]
			data4_temperature = data4['Temperature'][-1:].values
			data4_temperature_max = data4['Temperature'].max()
			data4_temperature_min = data4['Temperature'].min()
			data4_pressure = data4['Pressure'][-1:].values
			data4_pressure_max = data4['Pressure'].max()
			data4_pressure_min = data4['Pressure'].min()
			data4_humidity = data4['Humidity'][-1:].values
			data4_humidity_max = data4['Humidity'].max()
			data4_humidity_min = data4['Humidity'].min()
			data4_dewpoint = data4['Dewpoint'][-1:].values
			data4_dewpoint_max = data4['Dewpoint'].max()
			data4_dewpoint_min = data4['Dewpoint'].min()
			data4_voltage = data4['Voltage'][-1:].values
			data4_voltage_max = data4['Voltage'].max()
			data4_voltage_min = data4['Voltage'].min()
			data4_rssi = data4['RSSI'][-1:].values
			data4_rssi_max = data4['RSSI'].max()
			data4_rssi_min = data4['RSSI'].min()
			if verbose:
				print sensor4label, "Time of Data Read:\t", data4_readtime
				print sensor4label, "Temperature:\t", data4_temperature, "H:", data4_temperature_max, "L:", data4_temperature_min
				print sensor4label, "Pressure:\t", data4_pressure, "H:", data4_pressure_max, "L:", data4_pressure_min
				print sensor4label, "Humidity:\t", data4_humidity, "H:", data4_humidity_max, "L:", data4_humidity_min
				print sensor4label, "Dewpoint:\t", data4_dewpoint, "H:", data4_dewpoint_max, "L:", data4_dewpoint_min
				print sensor4label, "Voltage:\t\t", data4_voltage, "H:", data4_voltage_max, "L:", data4_voltage_min
				print sensor4label, "RSSI:\t\t", data4_rssi, "H:", data4_rssi_max, "L:", data4_rssi_min
	except Exception:
			print("DATA4 ERROR", today, now)
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)

def svg_update():
	try:
		tree = etree.parse(open(template_svg_filename, 'r'))
		if (0 <= data0_voltage < 80):
			for element in tree.iter():
				if element.tag.split("}")[1] == "path":
					if element.get("id") == "b00Bat4":
						element.attrib['class'] = 'st3'
					if element.get("id") == "b00Bat3":
						element.attrib['class'] = 'st3'
					if element.get("id") == "b00Bat2":
						element.attrib['class'] = 'st3'
					if element.get("id") == "b00Bat1":
						element.attrib['class'] = 'st3'
					if element.get("id") == "b00Bat0":
						element.attrib['class'] = ''
					if verbose:
						print(data0label, data0voltage, " - 0 to 80")

if(1):
	scheduler = BackgroundScheduler()
	scheduler.add_job(data_call, 'interval', seconds=30)
	
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
	
