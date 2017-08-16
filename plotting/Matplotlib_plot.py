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

sys.path.append('/home/pi/Power_Monitoring/')

from standards import *

temp_plot = True
press_plot = True
humid_plot = True
volt_plot = True
rssi_plot = True
dropbox_upload = True
verbose = False

######## GLOBAL VAR #######
#td = '48H'
line_width = 1.5
rssi_line_width = 1
label_offset = 3

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
			if verbose:
				print("No logfile for today found...", str(today))
		try:
			data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + yesterday.strftime("%Y-%m") + '/' + str(yesterday) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_yest_valid = True
		except Exception:
			data_yest_valid = False
			if verbose:
				print("No logfile for yesterday found...", str(yesterday))
		try:
			data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior2.strftime("%Y-%m") + '/' + str(prior2) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_2prior_valid = True
		except Exception:
			data_2prior_valid = False
			if verbose:
				print("No logfile for TWO days ago found...", str(prior2))
		try:
			data_3prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior3.strftime("%Y-%m") + '/' + str(prior3) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_3prior_valid = True
		except Exception:
			data_3prior_valid = False
			if verbose:
				print("No logfile for THREE days ago found...", str(prior3))
		try:
			data_4prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior4.strftime("%Y-%m") + '/' + str(prior4) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_4prior_valid = True
		except Exception:
			data_4prior_valid = False
			if verbose:
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
			if verbose:
				print("Data0 Error")
			data0 = None
		try:
			data1 = data.loc[data['Address'] == sensor1]
		except Exception:
			if verbose:
				print("Data1 Error")
			data1 = None
		try:
			data2 = data.loc[data['Address'] == sensor2]
		except Exception:
			if verbose:
				print("Data2 Error")
			data2 = None
		try:
			data3 = data.loc[data['Address'] == sensor3]
		except Exception:
			if verbose:
				print("Data3 Error")
			data3 = None
		try:
			data4 = data.loc[data['Address'] == sensor4]
		except Exception:
			if verbose:
				print("Data4 Error")
			data4 = None
		try:
			data5 = data.loc[data['Address'] == sensor5]
		except Exception:
			if verbose:
				print("Data5 Error")
			data5 = None
		try:
			data6 = data.loc[data['Address'] == sensor6]
		except Exception:
			if verbose:
				print("Data6 Error")
			data6 = None
		try:
			data7 = data.loc[data['Address'] == sensor7]
		except Exception:
			if verbose:
				print("Data7 Error")
			data7 = None
	except Exception:
		print("ERROR: CSV IMPORT/DATA INPUT", today, now)
		traceback.print_exc(file=sys.stdout)

def dataplot(datatype, timedelta):
	now = datetime.datetime.now()
	today = datetime.date.today()
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
		print("ERROR: PLOTTING %s ERROR" %datatype, today, now)
		traceback.print_exc(file=sys.stdout)

def dataplot_sm(datatype, timedelta, sensor):
	now = datetime.datetime.now()
	today = datetime.date.today()
	try:
		fig = plt.figure(figsize=(4.5, 1.875))
		plt.style.use('dark_background')
		matplotlib.rcParams.update({'font.size': 4})
		if not data0.empty and sensor == '0':
			plt.plot_date(data0.last(timedelta).index, data0[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color='w', label=sensor0label)
		if not data1.empty and sensor == '1':
			plt.plot_date(data1.last(timedelta).index, data1[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
		if not data2.empty and sensor == '2':
			plt.plot_date(data2.last(timedelta).index, data2[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
		if not data3.empty and sensor == '3':
			plt.plot_date(data3.last(timedelta).index, data3[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
		if not data4.empty and sensor == '4':
			plt.plot_date(data4.last(timedelta).index, data4[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
		if not data5.empty and sensor == '5':
			plt.plot_date(data5.last(timedelta).index, data5[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
		if not data6.empty and sensor == '6':
			plt.plot_date(data6.last(timedelta).index, data6[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
		if not data7.empty and sensor == '7':
			plt.plot_date(data7.last(timedelta).index, data7[datatype].last(timedelta).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
		plt.xlabel('Time')
		plt.ylabel(datatype)
		plt.grid(True)
		fig.text(0.5, 0.5, '%s ' %datatype, fontsize=14, color='white', ha='center', va='center', alpha=0.35)
		myFmt = mdates.DateFormatter('%H:%M')
		fig.axes[0].get_xaxis().set_major_formatter(myFmt)
		fig.autofmt_xdate()
		fig.savefig('/home/pi/Power_Monitoring/output/plot_sm_%s_sensor_%s.png' %(datatype, sensor), bbox_inches='tight')
		subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/plot_%s.png" %datatype])
		subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/plot_%s.png" %datatype, "/var/www/html/"])
		if dropbox_upload:
			subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/output/plot_%s.png" %datatype, "/Programming/logs/%s/plots/" %location])
	except Exception:
		print("ERROR: PLOTTING %s ERROR" %datatype, today, now)
		traceback.print_exc(file=sys.stdout)


if (1):
	datainput()
	dataplot('Temperature', td)
	dataplot('Pressure', td)
	dataplot('Humidity', td)
	dataplot('Voltage', td)
	dataplot('RSSI', td)
	dataplot('Dewpoint', td)
	dataplot_sm('Temperature', td, '0')
	dataplot_sm('Temperature', td, '1')
	dataplot_sm('Temperature', td, '2')
