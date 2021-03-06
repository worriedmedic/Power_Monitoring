import pandas as pd
import numpy as np
import datetime, time
import traceback
import sys, os.path
import codecs
import traceback
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import cPickle as pickle
logging.basicConfig()
from standards import *
import ephem

verbose = False
sensordata = True
weatherdata = False
dropbox_upload = True
now = datetime.datetime.now()

for arg in sys.argv:
	if arg == '-v':
		verbose = True
		print("VERBOSE IS ON")
	elif arg == '-drop_on':
		dropbox_upload = True
		print("DROPBOX UPLOADER IS ENABLED")
	elif arg == '-drop_off':
		dropbox_upload = False
		print("DROPBOX UPLOAD IS DISABLED")
	elif arg == '-h':
		print("SVG_Processing.py script - LWH & NHH")
		print("Backend processing of data collected by Arduino based sensors for output to SVG/PNG file")
		print("Options: [-v VERBOSE] [-h HELP] [-drop_on DROPBOX ENABLED] [-drop_off DROPBOX DISABLED")
		sys.exit()

def daily_wunder_update():
	while True:
		global forecast_data, astronomy_data
		now = datetime.datetime.now()
		try:
			forecast_data = pd.read_json(wunder_site_forecast_json, typ='series')
			astronomy_data = pd.read_json(wunder_site_astronomy_json, typ='series')
		except Exception:
			print("ERROR: DAILY WUNDER UPDATE", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			traceback.print_exc(file=sys.stdout)
			time.sleep(10)
			continue
		break

def hourly_wunder_update():
	while True:
		global condition_data
		now = datetime.datetime.now()
		try:
			condition_data = pd.read_json(wunder_site_conditions_json, typ='series')
		except Exception:
			print("ERROR: DAILY WUNDER UPDATE", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			traceback.print_exc(file=sys.stdout)
			time.sleep(10)
			continue
		break

def astro_data():
	try:
		global d
		d = {}
		dst = True
		cutty = ephem.Observer()
		cutty.lat = '41.42'
		cutty.long = '-70.92'
		cutty.elevation = 20
		if dst:
			dst_const = (ephem.hour * -4)
		else:
			dst_const = (ephem.hour * -5)
		planets = 	[ephem.Sun(),
				ephem.Moon(),
				ephem.Mars(),
				ephem.Jupiter(),
				ephem.Saturn(),
				ephem.Venus()]
		for o in planets:
			o.compute(cutty)
			if str(o.alt).startswith('-'):
				d[o.name] = {'name'	: o.name,
					    'visible'	: False,
					    'altitude'	: str(o.alt),
					    'azimuth'	: str(o.az),
					    'rising'	: ephem.Date(cutty.next_rising(o) + dst_const).datetime(),
					    'setting'	: ephem.Date(cutty.previous_setting(o) + dst_const).datetime()}
				if verbose:
					print('%s IS NOT VISIBLE' %d[o.name]['name'])
					print('%s: alt: %s azm: %s' %(d[o.name]['name'], d[o.name]['altitude'], d[o.name]['azimuth']))
					print('Next Rising: ', ephem.Date(cutty.next_rising(o) + dst_const))
					print('Previous Setting: ', ephem.Date(cutty.previous_setting(o) + dst_const))
			else:
				d[o.name] = {'name'	: o.name,
					    'visible'	: True,
					    'altitude'	: str(o.alt),
					    'azimuth'	: str(o.az),
					    'rising'	: ephem.Date(cutty.previous_rising(o) + dst_const).datetime(),
					    'setting'	: ephem.Date(cutty.next_setting(o) + dst_const).datetime()}
				if verbose:
					print('%s IS VISIBLE' %d[o.name]['name'])
					print('%s: alt: %s azm: %s' %(d[o.name]['name'], d[o.name]['altitude'], d[o.name]['azimuth']))
					print('Previous Rising: ', ephem.Date(cutty.previous_rising(o) + dst_const))
					print('Next Setting: ', ephem.Date(cutty.next_setting(o) + dst_const))
	except Exception:
		print("ERROR: ASTRO DATA", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)

def data_call():	
	today = datetime.date.today()
	now = datetime.datetime.now()
	now_minus_twentyfour = now + datetime.timedelta(hours=-24)
	today_minus_one = datetime.date.today() + datetime.timedelta(days=-1)
	today_minus_two = datetime.date.today() + datetime.timedelta(days=-2)
	today_minus_three = datetime.date.today() + datetime.timedelta(days=-3)
	today_plus_one = datetime.date.today() + datetime.timedelta(days=1)
	today_plus_two = datetime.date.today() + datetime.timedelta(days=2)
	today_plus_three = datetime.date.today() + datetime.timedelta(days=3)
	astro_data()
	if tide:
		try:
			global tide_data
			tide_begin_date = today_minus_one.strftime('%Y%m%d')
			tide_end_date = today_plus_one.strftime('%Y%m%d')
			tide_csv = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=%s&end_date=%s&datum=MLLW&station=8448376&time_zone=lst_ldt&units=english&interval=hilo&format=csv' %(tide_begin_date, tide_end_date)
			tides = pd.read_table(tide_csv, sep=',', skiprows=1, names = ["Datetime","Feet","High/Low"], dtype=str)
			tides['Datetime'] = pd.to_datetime(tides['Datetime'])
			tides = tides.set_index('Datetime')
			tides['Feet'] = tides['Feet'].astype(float)
			tide_data = {'tide_prior_time'	: tides['Feet'][:now.strftime("%Y-%m-%d %H:%M:%S")].index[-1],
				     'tide_prior_level'	: tides['Feet'][:now.strftime("%Y-%m-%d %H:%M:%S")][-1],
				     'tide_prior_type'	: tides['High/Low'][:now.strftime("%Y-%m-%d %H:%M:%S")][-1],
				     'tide_prior_count' : now - tides['Feet'][:now.strftime("%Y-%m-%d %H:%M:%S")].index[-1],
				     'tide_next_time'	: tides['Feet'][now.strftime("%Y-%m-%d %H:%M:%S"):].index[0],
				     'tide_next_level'	: tides['Feet'][now.strftime("%Y-%m-%d %H:%M:%S"):][0],
				     'tide_next_type'	: tides['High/Low'][now.strftime("%Y-%m-%d %H:%M:%S"):][0],
				     'tide_next_count'  : tides['Feet'][now.strftime("%Y-%m-%d %H:%M:%S"):].index[0] - now,
				     'tide_after_time'	: tides['Feet'][now.strftime("%Y-%m-%d %H:%M:%S"):].index[1],
				     'tide_after_level'	: tides['Feet'][now.strftime("%Y-%m-%d %H:%M:%S"):][1],
				     'tide_after_type'	: tides['High/Low'][now.strftime("%Y-%m-%d %H:%M:%S"):][1],
				     'tide_after_count' : tides['Feet'][now.strftime("%Y-%m-%d %H:%M:%S"):].index[1] - now}
			if verbose:
				print "Previous Tide:", tide_data['tide_prior_time'], tide_data['tide_prior_level'], str(tide_data['tide_prior_count'])[:7]
				print "Next Tide:", tide_data['tide_next_time'], tide_data['tide_next_level'], str(tide_data['tide_next_count'])[:7]
				print "Following Tide:", tide_data['tide_after_time'], tide_data['tide_after_level'], str(tide_data['tide_after_count'])[:7]
		except Exception:
			print("ERROR: TIDES", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			traceback.print_exc(file=sys.stdout)
	if weatherdata:
		try:			
			global weather_data
			weather_data = {'wind_mph'		: condition_data.current_observation['wind_mph'],
					'wind_gust'		: condition_data.current_observation['wind_gust_mph'],
					'wind_direction'	: condition_data.current_observation['wind_dir'],
					'pressure_trend'	: condition_data.current_observation['pressure_trend'],
					'forecast_high'		: forecast_data['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit'],
					'forecast_low'		: forecast_data['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit'],
					'sunrise'		: astronomy_data['sun_phase']['sunrise']['hour'] + ":" + astronomy_data['sun_phase']['sunrise']['minute'],
					'sunset'		: astronomy_data['sun_phase']['sunset']['hour'] + ":" + astronomy_data['sun_phase']['sunset']['minute']}
			if verbose:
				print location, "Wind (MPH):", weather_data['wind_mph'], "Wind Gust (MPH):", weather_data['wind_gust'], "Wind Direction:", weather_data['wind_direction'], "Pressure Trend:", weather_data['pressure_trend'], 
				print "Forecast High:", weather_data['forecast_high'], "Forecast Low:", weather_data['forecast_low']
				print "Sunrise: ", weather_data['sunrise'], "Sunset: ", weather_data['sunset']
		except Exception:
			print("ERROR: WEATHER DATA", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			traceback.print_exc(file=sys.stdout)
	if sensordata:
		try:
			if verbose:
				global data, data0, data1, data2, data3, data4, data5, data6, data7
			try:
				data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
				data_today_valid = True
			except Exception:
				data_today_valid = False
				if verbose:
					print("NO TODAY LOG FILE", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			try:
				data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today_minus_one.strftime("%Y-%m") + '/' + str(today_minus_one) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
				data_yest_valid = True
			except Exception:
				data_yest_valid = False
				if verbose:
					print("NO YESTERDAY LOG FILE", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			try:
				data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today_minus_two.strftime("%Y-%m") + '/' + str(today_minus_two) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
				data_2prior_valid = True
			except Exception:
				data_2prior_valid = False
				if verbose:
					print("NO 2DAYPRIOR LOG FILE", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			if (data_today_valid and data_yest_valid and data_2prior_valid):
				data = pd.concat([data_2prior, data_yest, data_today])
				if verbose:
					print("Logs for today, yesterday and day prior are present")
			elif (data_today_valid and data_yest_valid):
				data = pd.concat([data_yest, data_today])
				if verbose:
					print("Logs for today and yesterday are present")
			elif data_today_valid:
				data = data_today
				if verbose:
					print("Log for today only present")
			data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
			data = data.drop(['Date', 'Time'], 1)
			data = data.set_index('Datetime')
			data = data[now_minus_twentyfour.strftime("%Y-%m-%d %H:%M:%S"):now.strftime("%Y-%m-%d %H:%M:%S")]
			data['Temperature'] = data['Temperature'].str.replace('T', '')
			data['Pressure'] = data['Pressure'].str.replace('P', '')
			data['Humidity'] = data['Humidity'].str.replace('H', '')
			data['Voltage'] = data['Voltage'].str.replace('V', '')
			data['Address'] = data['Address'].astype(int)
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
			data5 = data.loc[data['Address'] == sensor5]
			data6 = data.loc[data['Address'] == sensor6]
			data7 = data.loc[data['Address'] == sensor7]
			
		except Exception:
			print("ERROR: Main Data Aggragate PANDAS", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			traceback.print_exc(file=sys.stdout)
	try:
		if not data0.empty:
			global data0_global
			data0_global = {'name'		: sensor0label,
				      'time' 		: data0.index[-1:][0], 
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
		else:
			data0_global = None
	except Exception:
		print("ERROR: DATA0", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data1.empty:
			global data1_global
			data1_global = {'name'		: sensor1label,
				      'time' 		: data1.index[-1:][0], 
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
		else:
			data1_global = None
	except Exception:
		print("ERROR: DATA1", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data2.empty:
			global data2_global
			data2_global = {'name'		: sensor2label,
				      'time' 		: data2.index[-1:][0], 
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
		else:
			data2_global = None
	except Exception:
		print("ERROR: DATA2", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data3.empty:
			global data3_global
			data3_global = {'name'		: sensor3label,
				      'time' 		: data3.index[-1:][0], 
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
		else:
			data3_global = None
	except Exception:
		print("ERROR: DATA3", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data4.empty:
			global data4_global
			data4_global = {'name'		: sensor4label,
				      'time' 		: data4.index[-1:][0], 
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
		else:
			data4_global = None
	except Exception:
		print("ERROR: DATA4", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data5.empty:
			global data5_global
			data5_global = {'name'		: sensor5label,
				      'time' 		: data5.index[-1:][0], 
				      'temperature'	: data5['Temperature'][-1:].values, 
				      'temperature_max'	: data5['Temperature'].max(),
				      'temperature_min' : data5['Temperature'].min(),
				      'pressure'	: data5['Pressure'][-1:].values,
				      'pressure_max'	: data5['Pressure'].max(),
				      'pressure_min'	: data5['Pressure'].min(),
				      'humidity'	: data5['Humidity'][-1:].values,
				      'humidity_max'	: data5['Humidity'].max(),
				      'humidity_min'	: data5['Humidity'].min(),
				      'dewpoint'	: data5['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data5['Dewpoint'].max(),
				      'dewpoint_min'	: data5['Dewpoint'].min(),
				      'voltage'		: data5['Voltage'][-1:].values,
				      'voltage_max'	: data5['Voltage'].max(),
				      'voltage_min'	: data5['Voltage'].min(),
				      'rssi'		: data5['RSSI'][-1:].values,
				      'rssi_max'	: data5['RSSI'].max(),
				      'rssi_min'	: data5['RSSI'].min()}
			if verbose:
				print sensor5label, "Time of Data Read:\t", data5_global['time']
				print sensor5label, "Temperature:\t", data5_global['temperature'], "H:", data5_global['temperature_max'], "L:", data5_global['temperature_min']
				print sensor5label, "Pressure:\t", data5_global['pressure'], "H:", data5_global['pressure_max'], "L:", data5_global['pressure_min']
				print sensor5label, "Humidity:\t", data5_global['humidity'], "H:", data5_global['humidity_max'], "L:", data5_global['humidity_min']
				print sensor5label, "Dewpoint:\t", data5_global['dewpoint'], "H:", data5_global['dewpoint_max'], "L:", data5_global['dewpoint_min']
				print sensor5label, "Voltage:\t\t", data5_global['voltage'], "H:", data5_global['voltage_max'], "L:", data5_global['voltage_min']
				print sensor5label, "RSSI:\t\t", data5_global['rssi'], "H:", data5_global['rssi_max'], "L:", data5_global['rssi_min']
		else:
			data5_global = None
	except Exception:
		print("ERROR: DATA5", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data6.empty:
			global data6_global
			data6_global = {'name'		: sensor6label,
				      'time' 		: data6.index[-1:][0], 
				      'temperature'	: data6['Temperature'][-1:].values, 
				      'temperature_max'	: data6['Temperature'].max(),
				      'temperature_min' : data6['Temperature'].min(),
				      'pressure'	: data6['Pressure'][-1:].values,
				      'pressure_max'	: data6['Pressure'].max(),
				      'pressure_min'	: data6['Pressure'].min(),
				      'humidity'	: data6['Humidity'][-1:].values,
				      'humidity_max'	: data6['Humidity'].max(),
				      'humidity_min'	: data6['Humidity'].min(),
				      'dewpoint'	: data6['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data6['Dewpoint'].max(),
				      'dewpoint_min'	: data6['Dewpoint'].min(),
				      'voltage'		: data6['Voltage'][-1:].values,
				      'voltage_max'	: data6['Voltage'].max(),
				      'voltage_min'	: data6['Voltage'].min(),
				      'rssi'		: data6['RSSI'][-1:].values,
				      'rssi_max'	: data6['RSSI'].max(),
				      'rssi_min'	: data6['RSSI'].min()}
			if verbose:
				print sensor6label, "Time of Data Read:\t", data6_global['time']
				print sensor6label, "Temperature:\t", data6_global['temperature'], "H:", data6_global['temperature_max'], "L:", data6_global['temperature_min']
				print sensor6label, "Pressure:\t", data6_global['pressure'], "H:", data6_global['pressure_max'], "L:", data6_global['pressure_min']
				print sensor6label, "Humidity:\t", data6_global['humidity'], "H:", data6_global['humidity_max'], "L:", data6_global['humidity_min']
				print sensor6label, "Dewpoint:\t", data6_global['dewpoint'], "H:", data6_global['dewpoint_max'], "L:", data6_global['dewpoint_min']
				print sensor6label, "Voltage:\t\t", data6_global['voltage'], "H:", data6_global['voltage_max'], "L:", data6_global['voltage_min']
				print sensor6label, "RSSI:\t\t", data6_global['rssi'], "H:", data6_global['rssi_max'], "L:", data6_global['rssi_min']
		else:
			data6_global = None
	except Exception:
		print("ERROR: DATA6", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	try:
		if not data7.empty:
			global data7_global
			data7_global = {'name'		: sensor7label,
				      'time' 		: data7.index[-1:][0], 
				      'temperature'	: data7['Temperature'][-1:].values, 
				      'temperature_max'	: data7['Temperature'].max(),
				      'temperature_min' : data7['Temperature'].min(),
				      'pressure'	: data7['Pressure'][-1:].values,
				      'pressure_max'	: data7['Pressure'].max(),
				      'pressure_min'	: data7['Pressure'].min(),
				      'humidity'	: data7['Humidity'][-1:].values,
				      'humidity_max'	: data7['Humidity'].max(),
				      'humidity_min'	: data7['Humidity'].min(),
				      'dewpoint'	: data7['Dewpoint'][-1:].values,
				      'dewpoint_max'	: data7['Dewpoint'].max(),
				      'dewpoint_min'	: data7['Dewpoint'].min(),
				      'voltage'		: data7['Voltage'][-1:].values,
				      'voltage_max'	: data7['Voltage'].max(),
				      'voltage_min'	: data7['Voltage'].min(),
				      'rssi'		: data7['RSSI'][-1:].values,
				      'rssi_max'	: data7['RSSI'].max(),
				      'rssi_min'	: data7['RSSI'].min()}
			if verbose:
				print sensor7label, "Time of Data Read:\t", data7_global['time']
				print sensor7label, "Temperature:\t", data7_global['temperature'], "H:", data7_global['temperature_max'], "L:", data7_global['temperature_min']
				print sensor7label, "Pressure:\t", data7_global['pressure'], "H:", data7_global['pressure_max'], "L:", data7_global['pressure_min']
				print sensor7label, "Humidity:\t", data7_global['humidity'], "H:", data7_global['humidity_max'], "L:", data7_global['humidity_min']
				print sensor7label, "Dewpoint:\t", data7_global['dewpoint'], "H:", data7_global['dewpoint_max'], "L:", data7_global['dewpoint_min']
				print sensor7label, "Voltage:\t\t", data7_global['voltage'], "H:", data7_global['voltage_max'], "L:", data7_global['voltage_min']
				print sensor7label, "RSSI:\t\t", data7_global['rssi'], "H:", data7_global['rssi_max'], "L:", data7_global['rssi_min']
		else:
			data7_global = None
	except Exception:
		print("ERROR: DATA7", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)
	txt_output()
	pickle_data()


def svg_update():
	try:
		today = datetime.date.today()
		now = datetime.datetime.now()
		output = codecs.open(template_svg_filename, 'r', encoding='utf-8').read()
		output = output.replace('CURDATE', today.strftime("%m/%d/%Y"))
		output = output.replace('CURTIME', now.strftime("%H:%M"))
		if weatherdata:
			output = output.replace('SNRISE', str(weather_data['sunrise']))
			output = output.replace('SNSET', str(weather_data['sunset']))
			output = output.replace('FORHI', str(weather_data['forecast_high']))
			output = output.replace('FORLO', str(weather_data['forecast_low']))
			output = output.replace('WSP', str(weather_data['wind_mph']))
			output = output.replace('WGUS', str(weather_data['wind_gust']))
			output = output.replace('WDIRECT', str(weather_data['wind_direction']))
		output = output.replace('TMP0LABEL', sensor0label)
		output = output.replace('TMP1LABEL', sensor1label)
		output = output.replace('TMP2LABEL', sensor2label)
		output = output.replace('TMP3LABEL', sensor3label)
		output = output.replace('TMP4LABEL', sensor4label)
		output = output.replace('TMP5LABEL', sensor5label)
		output = output.replace('TMP6LABEL', sensor6label)
		output = output.replace('TMP7LABEL', sensor7label)
		if data0_global:
			if data0_global['temperature'] >= 100:
				output = output.replace('TMP0TMP', "{0:.1f}".format(float(data0_global['temperature'])))
			elif data0_global['temperature'] < 100:
				output = output.replace('TMP0TMP', "{0:.2f}".format(float(data0_global['temperature'])))
			output = output.replace('TMP0TIME', str(data0_global['time']))
			output = output.replace('TMP0HI', "{0:.2f}".format(float(data0_global['temperature_max'])))
			output = output.replace('TMP0LO', "{0:.2f}".format(float(data0_global['temperature_min'])))
			if data0_global['pressure'] >= 1000:
				output = output.replace('TMP0PRESS', "{0:.0f}".format(float(data0_global['pressure'])))
			elif data0_global['pressure'] < 1000:
				output = output.replace('TMP0PRESS', "{0:.1f}".format(float(data0_global['pressure'])))
			if data0_global['humidity'] == 100:
				output = output.replace('TMP0RELHUM', "{0:.1f}".format(float(data0_global['humidity'])))
			elif data0_global['humidity'] < 100:
				output = output.replace('TMP0RELHUM', "{0:.2f}".format(float(data0_global['humidity'])))
			output = output.replace('TMP0DWPNT', "{0:.2f}".format(float(data0_global['dewpoint'])))
			output = output.replace('TMP0VOLT', "{0:.1f}".format(float(data0_global['voltage'])))
		else:
			output = output.replace('TMP0TMP', '00.00')
			output = output.replace('TMP0TIME', '00:00:00')
			output = output.replace('TMP0HI', '00.00')
			output = output.replace('TMP0LO', '00.00')
			output = output.replace('TMP0PRESS', '00.00')
			output = output.replace('TMP0RELHUM', '00.00')
			output = output.replace('TMP0DWPNT', '00.00')
			output = output.replace('TMP0VOLT', '00.00')
		if data1_global:
			if data1_global['temperature'] >= 100:
				output = output.replace('TMP1TMP', "{0:.1f}".format(float(data1_global['temperature'])))
			elif data1_global['temperature'] < 100:
				output = output.replace('TMP1TMP', "{0:.2f}".format(float(data1_global['temperature'])))
			output = output.replace('TMP1TIME', str(data1_global['time']))
			output = output.replace('TMP1HI', "{0:.2f}".format(float(data1_global['temperature_max'])))
			output = output.replace('TMP1LO', "{0:.2f}".format(float(data1_global['temperature_min'])))
			if data1_global['pressure'] >= 1000:
				output = output.replace('TMP1PRESS', "{0:.0f}".format(float(data1_global['pressure'])))
			elif data1_global['pressure'] < 1000:
				output = output.replace('TMP1PRESS', "{0:.1f}".format(float(data1_global['pressure'])))
			if data1_global['humidity'] == 100:
				output = output.replace('TMP1RELHUM', "{0:.1f}".format(float(data1_global['humidity'])))
			elif data1_global['humidity'] < 100:
				output = output.replace('TMP1RELHUM', "{0:.2f}".format(float(data1_global['humidity'])))
			output = output.replace('TMP1DWPNT', "{0:.2f}".format(float(data1_global['dewpoint'])))
			output = output.replace('TMP1VOLT', "{0:.1f}".format(float(data1_global['voltage'])))
		else:
			output = output.replace('TMP1TMP', '00.00')
			output = output.replace('TMP1TIME', '00:00:00')
			output = output.replace('TMP1HI', '00.00')
			output = output.replace('TMP1LO', '00.00')
			output = output.replace('TMP1PRESS', '00.00')
			output = output.replace('TMP1RELHUM', '00.00')
			output = output.replace('TMP1DWPNT', '00.00')
			output = output.replace('TMP1VOLT', '00.00')
		if data2_global:
			if data2_global['temperature'] >= 100:
				output = output.replace('TMP2TMP', "{0:.1f}".format(float(data2_global['temperature'])))
			elif data2_global['temperature'] < 100:
				output = output.replace('TMP2TMP', "{0:.2f}".format(float(data2_global['temperature'])))
			output = output.replace('TMP2TIME', str(data2_global['time']))
			output = output.replace('TMP2HI', "{0:.2f}".format(float(data2_global['temperature_max'])))
			output = output.replace('TMP2LO', "{0:.2f}".format(float(data2_global['temperature_min'])))
			output = output.replace('TMP2VOLT', "{0:.1f}".format(float(data2_global['voltage'])))
		else:
			output = output.replace('TMP2TMP', '00.00')
			output = output.replace('TMP2TIME', '00:00:00')
			output = output.replace('TMP2HI', '00.00')
			output = output.replace('TMP2LO', '00.00')
			output = output.replace('TMP2VOLT', '00.00')
		if data3_global:
			if data3_global['temperature'] >= 100:
				output = output.replace('TMP3TMP', "{0:.1f}".format(float(data3_global['temperature'])))
			elif data3_global['temperature'] < 100:
				output = output.replace('TMP3TMP', "{0:.2f}".format(float(data3_global['temperature'])))
			output = output.replace('TMP3TIME', str(data3_global['time']))
			output = output.replace('TMP3HI', "{0:.2f}".format(float(data3_global['temperature_max'])))
			output = output.replace('TMP3LO', "{0:.2f}".format(float(data3_global['temperature_min'])))
			output = output.replace('TMP3VOLT', "{0:.1f}".format(float(data3_global['voltage'])))
		else:
			output = output.replace('TMP3TMP', '00.00')
			output = output.replace('TMP3TIME', '00:00:00')
			output = output.replace('TMP3HI', '00.00')
			output = output.replace('TMP3LO', '00.00')
			output = output.replace('TMP3VOLT', '00.00')
		if data4_global:
			if data4_global['temperature'] >= 100:
				output = output.replace('TMP4TMP', "{0:.1f}".format(float(data4_global['temperature'])))
			elif data4_global['temperature'] < 100:
				output = output.replace('TMP4TMP', "{0:.2f}".format(float(data4_global['temperature'])))
			output = output.replace('TMP4TIME', str(data4_global['time']))
			output = output.replace('TMP4HI', "{0:.2f}".format(float(data4_global['temperature_max'])))
			output = output.replace('TMP4LO', "{0:.2f}".format(float(data4_global['temperature_min'])))
			output = output.replace('TMP4VOLT', "{0:.1f}".format(float(data4_global['voltage'])))
		else:
			output = output.replace('TMP4TMP', '00.00')
			output = output.replace('TMP4TIME', '00:00:00')
			output = output.replace('TMP4HI', '00.00')
			output = output.replace('TMP4LO', '00.00')
			output = output.replace('TMP4VOLT', '00.00')
		if data5_global:
			if data5_global['temperature'] >= 100:
				output = output.replace('TMP5TMP', "{0:.1f}".format(float(data5_global['temperature'])))
			elif data5_global['temperature'] < 100:
				output = output.replace('TMP5TMP', "{0:.2f}".format(float(data5_global['temperature'])))
			output = output.replace('TMP5TIME', str(data5_global['time']))
			output = output.replace('TMP5HI', "{0:.2f}".format(float(data5_global['temperature_max'])))
			output = output.replace('TMP5LO', "{0:.2f}".format(float(data5_global['temperature_min'])))
			output = output.replace('TMP5VOLT', "{0:.1f}".format(float(data5_global['voltage'])))
		else:
			output = output.replace('TMP5TMP', '00.00')
			output = output.replace('TMP5TIME', '00:00:00')
			output = output.replace('TMP5HI', '00.00')
			output = output.replace('TMP5LO', '00.00')
			output = output.replace('TMP5VOLT', '00.00')
		if data6_global:
			if data6_global['temperature'] >= 100:
				output = output.replace('TMP6TMP', "{0:.1f}".format(float(data6_global['temperature'])))
			elif data6_global['temperature'] < 100:
				output = output.replace('TMP6TMP', "{0:.2f}".format(float(data6_global['temperature'])))
			output = output.replace('TMP6TIME', str(data6_global['time']))
			output = output.replace('TMP6HI', "{0:.2f}".format(float(data6_global['temperature_max'])))
			output = output.replace('TMP6LO', "{0:.2f}".format(float(data6_global['temperature_min'])))
			output = output.replace('TMP6VOLT', "{0:.1f}".format(float(data6_global['voltage'])))
		else:
			output = output.replace('TMP6TMP', '00.00')
			output = output.replace('TMP6TIME', '00:00:00')
			output = output.replace('TMP6HI', '00.00')
			output = output.replace('TMP6LO', '00.00')
			output = output.replace('TMP6VOLT', '00.00')
		if data7_global:
			if data7_global['temperature'] >= 100:
				output = output.replace('TMP7TMP', "{0:.1f}".format(float(data7_global['temperature'])))
			elif data7_global['temperature'] < 100:
				output = output.replace('TMP7TMP', "{0:.2f}".format(float(data7_global['temperature'])))
			output = output.replace('TMP7TIME', str(data7_global['time']))
			output = output.replace('TMP7HI', "{0:.2f}".format(float(data7_global['temperature_max'])))
			output = output.replace('TMP7LO', "{0:.2f}".format(float(data7_global['temperature_min'])))
			output = output.replace('TMP7VOLT', "{0:.1f}".format(float(data7_global['voltage'])))
		else:
			output = output.replace('TMP7TMP', '00.00')
			output = output.replace('TMP7TIME', '00:00:00')
			output = output.replace('TMP7HI', '00.00')
			output = output.replace('TMP7LO', '00.00')
			output = output.replace('TMP7VOLT', '00.00')
		if tide:
			output = output.replace('TDLSTM', str(tide_data['tide_prior_time'].strftime('%H:%M')))
			output = output.replace('TDLSHGT', str(tide_data['tide_prior_level']))
			output = output.replace('TDLSTYP', str(tide_data['tide_prior_type']))
			output = output.replace('TDLSCNT', str(tide_data['tide_prior_count'])[:4])
			output = output.replace('TDNXTM', str(tide_data['tide_next_time'].strftime('%H:%M')))
			output = output.replace('TDNXHGT', str(tide_data['tide_next_level']))
			output = output.replace('TDNXTYP', str(tide_data['tide_next_type']))
			output = output.replace('TDNXCNT', str(tide_data['tide_next_count'])[:4])
			output = output.replace('TDAFTM', str(tide_data['tide_after_time'].strftime('%H:%M')))
			output = output.replace('TDAFHGT', str(tide_data['tide_after_level']))
			output = output.replace('TDAFTYP', str(tide_data['tide_after_type']))
			output = output.replace('TDAFCNT', str(tide_data['tide_after_count'])[:4])
		codecs.open('/home/pi/Power_Monitoring/output/weather-script-output.svg', 'w', encoding='utf-8').write(output)
		subprocess.call(["rsvg-convert", "-b", "white", "-o", "/home/pi/Power_Monitoring/output/weather-script-output.png", "/home/pi/Power_Monitoring/output/weather-script-output.svg"])
		subprocess.call(["pngcrush", "-q", "-c", "0", "-ow /home/pi/Power_Monitoring/output/weather-script-output.png"])
		subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/weather-script-output.png"])
		subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/weather-script-output.svg"])
		subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/weather-script-output.png", "/var/www/html/"])
		subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/weather-script-output.svg", "/var/www/html/"])	 
	except Exception:
		print("ERROR: CODECS TO SVG", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)

def txt_output():
	now = datetime.datetime.now()
	try:
		with open("/home/pi/Power_Monitoring/output/weather_output.txt", "w") as text_file:
			text_file.write("Location: %s, Time: %s\n" %(location,now,))
			if weatherdata:
				text_file.write("Forecast High: %s Forecast Low: %s, Wind (MPH): %s Wind Gust (MPH): %s Wind Direction: %s\n" %(weather_data['forecast_high'], weather_data['forecast_low'],weather_data['wind_mph'], weather_data['wind_gust'], weather_data['wind_direction']))
				text_file.write("Pressure Trend:\t\t\t %s\n" %(weather_data['pressure_trend']))
			for o in d:
				if str(d[o]['altitude']).startswith('-'):
					text_file.write('%s is NOT visible alt: %s azm: %s Next Rise: %s Previous Set: %s\n' %(d[o]['name'], d[o]['altitude'], d[o]['azimuth'],d[o]['rising'], d[o]['setting']))
				else:
					text_file.write('%s is VISIBLE alt: %s azm: %s Previous Rise: %s Next Set: %s\n' %(d[o]['name'], d[o]['altitude'], d[o]['azimuth'],d[o]['rising'], d[o]['setting']))
			if tide:
				text_file.write("Previous Tide:\t\t\t %s %s %s %s\n" %(tide_data['tide_prior_time'], tide_data['tide_prior_level'], tide_data['tide_prior_type'], str(now - tide_data['tide_prior_time'])))
				text_file.write("Next Tide:\t\t\t %s %s %s %s\n" %(tide_data['tide_next_time'], tide_data['tide_next_level'], tide_data['tide_next_type'], str(tide_data['tide_next_time'] - now)))
				text_file.write("Following Tide:\t\t\t %s %s %s %s\n" %(tide_data['tide_after_time'], tide_data['tide_after_level'], tide_data['tide_after_type'], str(tide_data['tide_after_time'] - now)))
			if data0_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor0label, data0_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor0label, data0_global['temperature'], data0_global['temperature_max'], data0_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor0label, data0_global['pressure'], data0_global['pressure_max'], data0_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor0label, data0_global['humidity'], data0_global['humidity_max'], data0_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor0label, data0_global['dewpoint'], data0_global['dewpoint_max'], data0_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t %s\t\t  H: %s L: %s\n" %(sensor0label, data0_global['voltage'], data0_global['voltage_max'], data0_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor0label, data0_global['rssi'], data0_global['rssi_max'], data0_global['rssi_min']))
			if data1_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor1label, data1_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor1label, data1_global['temperature'], data1_global['temperature_max'], data1_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor1label, data1_global['pressure'], data1_global['pressure_max'], data1_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor1label, data1_global['humidity'], data1_global['humidity_max'], data1_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor1label, data1_global['dewpoint'], data1_global['dewpoint_max'], data1_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t %s\t\t  H: %s L: %s\n" %(sensor1label, data1_global['voltage'], data1_global['voltage_max'], data1_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor1label, data1_global['rssi'], data1_global['rssi_max'], data1_global['rssi_min']))
			if data2_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor2label, data2_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor2label, data2_global['temperature'], data2_global['temperature_max'], data2_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor2label, data2_global['pressure'], data2_global['pressure_max'], data2_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor2label, data2_global['humidity'], data2_global['humidity_max'], data2_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor2label, data2_global['dewpoint'], data2_global['dewpoint_max'], data2_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t %s\t\t  H: %s L: %s\n" %(sensor2label, data2_global['voltage'], data2_global['voltage_max'], data2_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor2label, data2_global['rssi'], data2_global['rssi_max'], data2_global['rssi_min']))
			if data3_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor3label, data3_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor3label, data3_global['temperature'], data3_global['temperature_max'], data3_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor3label, data3_global['pressure'], data3_global['pressure_max'], data3_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor3label, data3_global['humidity'], data3_global['humidity_max'], data3_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor3label, data3_global['dewpoint'], data3_global['dewpoint_max'], data3_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t\t %s\t\t  H: %s L: %s\n" %(sensor3label, data3_global['voltage'], data3_global['voltage_max'], data3_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor3label, data3_global['rssi'], data3_global['rssi_max'], data3_global['rssi_min']))
			if data4_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor4label, data4_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor4label, data4_global['temperature'], data4_global['temperature_max'], data4_global['temperature_min']))
				text_file.write("%s Pressure:\t\t\t %s\t\t  H: %s L: %s\n" %(sensor4label, data4_global['pressure'], data4_global['pressure_max'], data4_global['pressure_min']))
				text_file.write("%s Humidity:\t\t\t %s\t\t  H: %s L: %s\n" %(sensor4label, data4_global['humidity'], data4_global['humidity_max'], data4_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t\t %s\t\t  H: %s L: %s\n" %(sensor4label, data4_global['dewpoint'], data4_global['dewpoint_max'], data4_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t\t %s\t\t  H: %s L: %s\n" %(sensor4label, data4_global['voltage'], data4_global['voltage_max'], data4_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor4label, data4_global['rssi'], data4_global['rssi_max'], data4_global['rssi_min']))
			if data5_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor5label, data5_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor5label, data5_global['temperature'], data5_global['temperature_max'], data5_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor5label, data5_global['pressure'], data5_global['pressure_max'], data5_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor5label, data5_global['humidity'], data5_global['humidity_max'], data5_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor5label, data5_global['dewpoint'], data5_global['dewpoint_max'], data5_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t %s\t\t  H: %s L: %s\n" %(sensor5label, data5_global['voltage'], data5_global['voltage_max'], data5_global['voltage_min']))
				text_file.write("%s RSSI:\t\t %s\t\t\t  H: %s L: %s\n" %(sensor5label, data5_global['rssi'], data5_global['rssi_max'], data5_global['rssi_min']))
			if data6_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor6label, data6_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor6label, data6_global['temperature'], data6_global['temperature_max'], data6_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor6label, data6_global['pressure'], data6_global['pressure_max'], data6_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor6label, data6_global['humidity'], data6_global['humidity_max'], data6_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor6label, data6_global['dewpoint'], data6_global['dewpoint_max'], data6_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t %s\t\t  H: %s L: %s\n" %(sensor6label, data6_global['voltage'], data6_global['voltage_max'], data6_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor6label, data6_global['rssi'], data6_global['rssi_max'], data6_global['rssi_min']))
			if data7_global:
				text_file.write("%s Time of Data Read:\t %s\n" %(sensor7label, data7_global['time']))
				text_file.write("%s Temperature:\t\t %s\t\t  H: %s L: %s\n" %(sensor7label, data7_global['temperature'], data7_global['temperature_max'], data7_global['temperature_min']))
				text_file.write("%s Pressure:\t\t %s\t\t  H: %s L: %s\n" %(sensor7label, data7_global['pressure'], data7_global['pressure_max'], data7_global['pressure_min']))
				text_file.write("%s Humidity:\t\t %s\t\t  H: %s L: %s\n" %(sensor7label, data7_global['humidity'], data7_global['humidity_max'], data7_global['humidity_min']))
				text_file.write("%s Dewpoint:\t\t %s\t\t  H: %s L: %s\n" %(sensor7label, data7_global['dewpoint'], data7_global['dewpoint_max'], data7_global['dewpoint_min']))
				text_file.write("%s Voltage:\t\t %s\t\t  H: %s L: %s\n" %(sensor7label, data7_global['voltage'], data7_global['voltage_max'], data7_global['voltage_min']))
				text_file.write("%s RSSI:\t\t\t %s\t\t\t  H: %s L: %s\n" %(sensor7label, data7_global['rssi'], data7_global['rssi_max'], data7_global['rssi_min']))
		subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/weather_output.txt"])
		subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/weather_output.txt", "/var/www/html/"])
	except Exception:
		print("ERROR: TXT_OUTPUT()", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)

def dropbox_update():
	try:
		subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/output/weather_output.txt", "/Programming/logs/%s/" %location])
		subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/total_%s.p" %location, "/Programming/logs/%s/" %location])
	except Exception:
		print("ERROR: DROPBOX UPLOADING", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)


def pickle_data():
	try:
		if tide:
			total_pickle = {'0':data0_global, 
					'1':data1_global, 
					'2':data2_global, 
					'3':data3_global, 
					'4':data4_global, 
					'5':data5_global, 
					'6':data6_global, 
					'7':data7_global, 
					'tide':tide_data, 
					'astro':d}
		else:
			total_pickle = {'0':data0_global, 
					'1':data1_global, 
					'2':data2_global, 
					'3':data3_global, 
					'4':data4_global, 
					'5':data5_global, 
					'6':data6_global, 
					'7':data7_global, 
					'astro':d}
		dir_location = '/home/pi/Power_Monitoring/'
		pickle.dump(total_pickle, open(os.path.join(dir_location, 'total_%s.p' %location), 'wb'))
		if verbose:
			print("Pickled Dumped", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	except Exception:
		print("ERROR: PICKLE", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)

if(1):
	scheduler = BlockingScheduler()
	#scheduler.add_job(daily_wunder_update, 'cron', hour=0, minute=5)
	#scheduler.add_job(hourly_wunder_update, 'cron', hour='*/6')
	scheduler.add_job(svg_update, 'interval', seconds=5)
	scheduler.add_job(data_call, 'interval', seconds=30)
	if dropbox_upload:
		scheduler.add_job(dropbox_update, 'interval', minutes=5)
	try:
		#daily_wunder_update()
		#hourly_wunder_update()
		astro_data()
		data_call()
		dropbox_update()
		pickle_data()
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		scheduler.shutdown()
