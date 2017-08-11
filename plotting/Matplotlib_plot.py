import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time, datetime
import traceback
import sys, os.path
import subprocess

temp_plot = True
press_plot = True
humid_plot = True
volt_plot = True
rssi_plot = True
dropbox_upload = True

######## GLOBAL VAR #######
#td = '48H'
line_width = 1.5
rssi_line_width = 1
label_offset = 3

if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
	location     = 'Dover'
	td           = '48H'
	plt_size_x   = 10
	plt_size_y   = 8
	plt_size_dpi = 100
	plot_style   = 'bmh' 
	sensor0      = 9
	sensor0label = 'Outside'
	sensor1      = 8
	sensor1label = 'Upstairs'
	sensor2      = 7
	sensor2label = 'MBedroom'
	sensor3      = 6
	sensor3label = 'Garage'
	sensor4      = 5
	sensor4label = 'Guest'
	sensor5      = 4
	sensor5label = 'Downstairs'
	sensor6	     = 3
	sensor6label = 'Laundry'
	sensor7      = 2
	sensor7label = 'Liam'
elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
	location     = 'Cuttyhunk'
	td           = '72H'
	plt_size_x   = 10
	plt_size_y   = 8
	plt_size_dpi = 100
	plot_style   = 'bmh'
	sensor0	     = '98'
	sensor0label = 'Outside'
	sensor1	     = '96'
	sensor1label = 'Upstairs'
	sensor2	     = '95'
	sensor2label = 'Reeds Room'
	sensor3	     = '97'
	sensor3label = 'Barn'
	sensor4	     = '99'
	sensor4label = 'TEST'
	sensor5	     = None
	sensor5label = 'None'
	sensor6	     = None
	sensor6label = 'None'
	sensor7	     = None
	sensor7label = 'None'

def datainput():
	global data0, data1, data2, data3, data4, data5, data6, data7
	today = datetime.date.today()
	yesterday = datetime.date.today() + datetime.timedelta(days=-1)
	prior2 = datetime.date.today() + datetime.timedelta(days=-2)
	prior3 = datetime.date.today() + datetime.timedelta(days=-3)
	prior4 = datetime.date.today() + datetime.timedelta(days=-4)
	now = datetime.datetime.now()
	now_minus_eight = now + datetime.timedelta(hours=-8)
	try:
		try:
			data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_today_valid = True
		except Exception:
			data_today_valid = False
			print("No logfile for today found...", str(today))
		try:
			data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + yesterday.strftime("%Y-%m") + '/' + str(yesterday) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_yest_valid = True
		except Exception:
			data_yest_valid = False
			print("No logfile for yesterday found...", str(yesterday))
		try:
			data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior2.strftime("%Y-%m") + '/' + str(prior2) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_2prior_valid = True
		except Exception:
			data_2prior_valid = False
			print("No logfile for TWO days ago found...", str(prior2))
		try:
			data_3prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior3.strftime("%Y-%m") + '/' + str(prior3) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_3prior_valid = True
		except Exception:
			data_3prior_valid = False
			print("No logfile for THREE days ago found...", str(prior3))
		try:
			data_4prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior4.strftime("%Y-%m") + '/' + str(prior4) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_4prior_valid = True
		except Exception:
			data_4prior_valid = False
			print("No logfile for FOUR days ago found...", str(prior4))
		if (data_today_valid and data_yest_valid and data_2prior_valid and data_3prior_valid and data_4prior_valid):
			data = pd.concat([data_4prior, data_3prior, data_2prior, data_yest, data_today])
		elif (data_today_valid and data_yest_valid and data_2prior_valid and data_3prior_valid):
			data = pd.concat([data_3prior, data_2prior, data_yest, data_today])
		elif (data_today_valid and data_yest_valid and data_2prior_valid):
			data = pd.concat([data_2prior, data_yest, data_today])
		elif (data_today_valid and data_yest_valid):
			data = pd.concat([data_yest, data_today])
		elif data_today_valid:
			data = data_today
		else:
			print("No data logfiles found...")
			sys.exit(1)
		data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
		data = data.drop(['Date', 'Time'], 1)
		data = data.set_index('Datetime')
		data['Temperature'] = data['Temperature'].str.replace('T', '')
		data['Pressure'] = data['Pressure'].str.replace('P', '')
		data['Humidity'] = data['Humidity'].str.replace('H', '')
		data['Voltage'] = data['Voltage'].str.replace('V', '')
		data = data.convert_objects(convert_numeric=True)
		data['Dewpoint'] = data['Temperature'].values - (0.36 * (100 - data['Humidity'].values))
		try:
			data0 = data.loc[data['Address'] == sensor0]
		except Exception:
			print("Data0 Error")
		try:
			data1 = data.loc[data['Address'] == sensor1]
		except Exception:
			print("Data1 Error")
		try:
			data2 = data.loc[data['Address'] == sensor2]
		except Exception:
			print("Data2 Error")
		try:
			data3 = data.loc[data['Address'] == sensor3]
		except Exception:
			print("Data3 Error")
		try:
			data4 = data.loc[data['Address'] == sensor4]
		except Exception:
			print("Data4 Error")
		try:
			data5 = data.loc[data['Address'] == sensor5]
		except Exception:
			print("Data5 Error")
		try:
			data6 = data.loc[data['Address'] == sensor6]
		except Exception:
			print("Data6 Error")
		try:
			data7 = data.loc[data['Address'] == sensor7]
		except Exception:
			print("Data7 Error")		
	except Exception:
		print("TODAY READ CSV ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

def dataplot(datatype, timedelta):
	try:
		fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
		plt.style.use(plot_style)
		plt.rcParams['axes.facecolor']='w'
		if not data0.empty:
			plt.plot_date(data0.last(timedelta).index, data0[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
			plt.text(data0.index[-1:][0], data0[datatype][-1], data0[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
		if not data1.empty:
			plt.plot_date(data1.last(timedelta).index, data1[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
			plt.text(data1.index[-1:][0], data1[datatype][-1], data1[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][1])
		if not data2.empty:
			plt.plot_date(data2.last(timedelta).index, data2[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
			plt.text(data2.index[-1:][0], data2[datatype][-1], data2[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][2])
		if not data3.empty:
			plt.plot_date(data3.last(timedelta).index, data3[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
			plt.text(data3.index[-1:][0], data3[datatype][-1], data3[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][3])
		if not data4.empty:
			plt.plot_date(data4.last(timedelta).index, data4[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
			plt.text(data4.index[-1:][0], data4[datatype][-1], data4[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][4])
		if not data5.empty:
			plt.plot_date(data5.last(timedelta).index, data5[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
			plt.text(data5.index[-1:][0], data5[datatype][-1], data5[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][5])
		if not data6.empty:
			plt.plot_date(data6.last(timedelta).index, data6[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
			plt.text(data6.index[-1:][0], data6[datatype][-1], data6[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][6])
		if not data7.empty:
			plt.plot_date(data7.last(timedelta).index, data7[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
			plt.text(data7.index[-1:][0], data7[datatype][-1], data7[datatype][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][7])
		plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
		plt.title('%s Plot: Past %s' %(datatype, timedelta))
		plt.xlabel('Time')
		plt.ylabel(datatype)
		plt.grid(True)
		plt.tight_layout()
		myFmt = mdates.DateFormatter('%m-%d %H:%M')
		fig.axes[0].get_xaxis().set_major_formatter(myFmt)
		fig.autofmt_xdate()
		fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
		fig.savefig('/home/pi/Power_Monitoring/output/plot_%s.png' %datatype, bbox_inches='tight')
		subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/plot_%s.png" %datatype])
		subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/plot_%s.png" %datatype, "/var/www/html/"])
		if dropbox_upload:
			subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/output/plot_%s.png" %datatype, "/Programming/logs/%s/plots/" %location])
	except Exception:
		print("PLOTTING %s ERROR" %datatype)
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

if (1):
	datainput()
	dataplot('Temperature', td)
	dataplot('Pressure', td)
	dataplot('Humidity', td)
	dataplot('Voltage', td)
	dataplot('RSSI', td)
	dataplot('Dewpoint', td)
