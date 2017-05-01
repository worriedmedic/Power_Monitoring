import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys, os.path
from scipy.interpolate import interp1d

temp_plot = True
press_plot = True
humid_plot = True
volt_plot = True
rssi_plot = True

######## GLOBAL VAR #######
td = '30m'
line_width = 2
rssi_line_width = 1
label_offset = 3

if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
	location     = 'Dover'
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
	plt_size_x   = 6.5
	plt_size_y   = 9
	plt_size_dpi = 84
	plot_style   = 'grayscale'
	sensor0      = 94
	sensor0label = 'Outside'
	sensor1      = 95
	sensor1label = 'Upstairs'
	sensor2      = 96
	sensor2label = 'Reeds Room'
	sensor3      = 97
	sensor3label = 'Barn'
	sensor4      = 98
	sensor4label = 'Barn Upstairs' 
	sensor5		= 99
	sensor5label	= 'TEST'
	sensor6		= 93
	sensor6label	= 'None'
	sensor7		= 92
	sensor7label	= 'None'

if (1):
	today = datetime.date.today()
	yesterday = datetime.date.today() + datetime.timedelta(days=-1)
	prior2 = datetime.date.today() + datetime.timedelta(days=-2)
	prior3 = datetime.date.today() + datetime.timedelta(days=-3)
	now = datetime.datetime.now()
	now_minus_eight = now + datetime.timedelta(hours=-8)
	try:
		try:
			data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_today_valid = True
		except Exception:
			data_today_valid = False
			print("No logfile for today found...")
		try:
			data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + yesterday.strftime("%Y-%m") + '/' + str(yesterday) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_yest_valid = True
		except Exception:
			data_yest_valid = False
			print("No logfile for yesterday found...")
		try:
			data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior2.strftime("%Y-%m") + '/' + str(prior2) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
			data_2prior_valid = True
		except Exception:
			data_2prior_valid = False
			print("No logfile for two days ago found...")
		if (data_today_valid and data_yest_valid and data_2prior_valid):
			data = pd.concat([data_2prior, data_yest, data_today])
		elif (data_today_valid and data_yest_valid):
			data = pd.concat([data_yest, data_today])
		elif data_today_valid:
			data = data_today
		else:
			print("No data logfiles found...")
		data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
		data = data.drop(['Date', 'Time'], 1)
		data = data.set_index('Datetime')
		data['Temperature'] = data['Temperature'].str.replace('T', '')
		data['Pressure'] = data['Pressure'].str.replace('P', '')
		data['Humidity'] = data['Humidity'].str.replace('H', '')
		data['Voltage'] = data['Voltage'].str.replace('V', '')
		data = data.convert_objects(convert_numeric=True)
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
	try:
		if temp_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
			plt.style.use(plot_style)
			plt.rcParams['axes.facecolor']='w'
			if not data0.empty:
				plt.plot_date(data0.last(td).index, data0['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
				plt.text(data0.index[-1:][0], data0['Temperature'][-1], data0['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
				#plt.text(data0.index[-1:][0], data0['Temperature'][-1] + label_offset, sensor0label, fontsize=12, color=plt.rcParams['axes.color_cycle'][0])
			if not data1.empty:
				plt.plot_date(data1.last(td).index, data1['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
				plt.text(data1.index[-1:][0], data1['Temperature'][-1], data1['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][1])
				#plt.text(data1.index[-1:][0], data1['Temperature'][-1] + label_offset, sensor1label, fontsize=12, color=plt.rcParams['axes.color_cycle'][1])
			if not data2.empty:
				plt.plot_date(data2.last(td).index, data2['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
				plt.text(data2.index[-1:][0], data2['Temperature'][-1], data2['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][2])
				#plt.text(data2.index[-1:][0], data2['Temperature'][-1] + label_offset, sensor2label, fontsize=12, color=plt.rcParams['axes.color_cycle'][2])
			if not data3.empty:
				plt.plot_date(data3.last(td).index, data3['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
				plt.text(data3.index[-1:][0], data3['Temperature'][-1], data3['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][3])
				#plt.text(data3.index[-1:][0], data3['Temperature'][-1] + label_offset, sensor3label, fontsize=12, color=plt.rcParams['axes.color_cycle'][3])
			if not data4.empty:
				plt.plot_date(data4.last(td).index, data4['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
				plt.text(data4.index[-1:][0], data4['Temperature'][-1], data4['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][4])
				#plt.text(data4.index[-1:][0], data4['Temperature'][-1] + label_offset, sensor4label, fontsize=12, color=plt.rcParams['axes.color_cycle'][4])
			if not data5.empty:
				plt.plot_date(data5.last(td).index, data5['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
				plt.text(data5.index[-1:][0], data5['Temperature'][-1], data5['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][5])
				#plt.text(data5.index[-1:][0], data5['Temperature'][-1] + label_offset, sensor5label, fontsize=12, color=plt.rcParams['axes.color_cycle'][5])
			if not data6.empty:
				plt.plot_date(data6.last(td).index, data6['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
				plt.text(data6.index[-1:][0], data6['Temperature'][-1], data6['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][6])
				#plt.text(data6.index[-1:][0], data6['Temperature'][-1] + label_offset, sensor6label, fontsize=12, color=plt.rcParams['axes.color_cycle'][6])
			if not data7.empty:
				plt.plot_date(data7.last(td).index, data7['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
				plt.text(data7.index[-1:][0], data7['Temperature'][-1], data7['Temperature'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][7])
			plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
			plt.title('Temperature Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Temp (F)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
			fig.savefig('/home/pi/Power_Monitoring/output/plot_temp.png', bbox_inches='tight')
		if press_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
			plt.style.use(plot_style)
			plt.rcParams['axes.facecolor']='w'
			if not data0.empty:
				plt.plot_date(data0.last(td).index, data0['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
				plt.text(data0.index[-1:][0], data0['Pressure'][-1], data0['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
				#plt.text(data0.index[-1:][0], data0['Pressure'][-1] + label_offset, sensor0label, fontsize=12, color=plt.rcParams['axes.color_cycle'][0])
			if not data1.empty:
				plt.plot_date(data1.last(td).index, data1['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
				plt.text(data1.index[-1:][0], data1['Pressure'][-1], data1['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][1])
				#plt.text(data1.index[-1:][0], data1['Pressure'][-1] + label_offset, sensor1label, fontsize=12, color=plt.rcParams['axes.color_cycle'][1])
			if not data2.empty:
				plt.plot_date(data2.last(td).index, data2['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
				plt.text(data2.index[-1:][0], data2['Pressure'][-1], data2['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][2])
				#plt.text(data2.index[-1:][0], data2['Pressure'][-1] + label_offset, sensor2label, fontsize=12, color=plt.rcParams['axes.color_cycle'][2])
			if not data3.empty:
				plt.plot_date(data3.last(td).index, data3['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
				plt.text(data3.index[-1:][0], data3['Pressure'][-1], data3['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][3])
				#plt.text(data3.index[-1:][0], data3['Pressure'][-1] + label_offset, sensor3label, fontsize=12, color=plt.rcParams['axes.color_cycle'][3])
			if not data4.empty:
				plt.plot_date(data4.last(td).index, data4['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
				plt.text(data4.index[-1:][0], data4['Pressure'][-1], data4['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][4])
				#plt.text(data4.index[-1:][0], data4['Pressure'][-1] + label_offset, sensor4label, fontsize=12, color=plt.rcParams['axes.color_cycle'][4])
			if not data5.empty:
				plt.plot_date(data5.last(td).index, data5['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
				plt.text(data5.index[-1:][0], data5['Pressure'][-1], data5['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][5])
				#plt.text(data5.index[-1:][0], data5['Pressure'][-1] + label_offset, sensor5label, fontsize=12, color=plt.rcParams['axes.color_cycle'][5])
			if not data6.empty:
				plt.plot_date(data6.last(td).index, data6['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
				plt.text(data6.index[-1:][0], data6['Pressure'][-1], data6['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][6])
				#plt.text(data6.index[-1:][0], data6['Pressure'][-1] + label_offset, sensor6label, fontsize=12, color=plt.rcParams['axes.color_cycle'][6])
			if not data7.empty:
				plt.plot_date(data7.last(td).index, data7['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
				plt.text(data7.index[-1:][0], data7['Pressure'][-1], data7['Pressure'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][7])
			plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
			plt.title('Pressure Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Pressure (hPa)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
			fig.savefig('/home/pi/Power_Monitoring/output/plot_press.png', bbox_inches='tight')
		if humid_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
			plt.style.use(plot_style)
			plt.rcParams['axes.facecolor']='w'
			if not data0.empty:
				plt.plot_date(data0.last(td).index, data0['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
				plt.text(data0.index[-1:][0], data0['Humidity'][-1], data0['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
				#plt.text(data0.index[-1:][0], data0['Humidity'][-1] + label_offset, sensor0label, fontsize=12, color=plt.rcParams['axes.color_cycle'][0])
			if not data1.empty:
				plt.plot_date(data1.last(td).index, data1['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
				plt.text(data1.index[-1:][0], data1['Humidity'][-1], data1['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][1])
				#plt.text(data1.index[-1:][0], data1['Humidity'][-1] + label_offset, sensor1label, fontsize=12, color=plt.rcParams['axes.color_cycle'][1])
			if not data2.empty:
				plt.plot_date(data2.last(td).index, data2['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
				plt.text(data2.index[-1:][0], data2['Humidity'][-1], data2['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][2])
				#plt.text(data2.index[-1:][0], data2['Humidity'][-1] + label_offset, sensor2label, fontsize=12, color=plt.rcParams['axes.color_cycle'][2])
			if not data3.empty:
				plt.plot_date(data3.last(td).index, data3['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
				plt.text(data3.index[-1:][0], data3['Humidity'][-1], data3['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][3])
				#plt.text(data3.index[-1:][0], data3['Humidity'][-1] + label_offset, sensor3label, fontsize=12, color=plt.rcParams['axes.color_cycle'][3])
			if not data4.empty:
				plt.plot_date(data4.last(td).index, data4['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
				plt.text(data4.index[-1:][0], data4['Humidity'][-1], data4['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][4])
				#plt.text(data4.index[-1:][0], data4['Humidity'][-1] + label_offset, sensor4label, fontsize=12, color=plt.rcParams['axes.color_cycle'][4])
			if not data5.empty:
				plt.plot_date(data5.last(td).index, data5['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
				plt.text(data5.index[-1:][0], data5['Humidity'][-1], data5['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][5])
				#plt.text(data5.index[-1:][0], data5['Humidity'][-1] + label_offset, sensor5label, fontsize=12, color=plt.rcParams['axes.color_cycle'][5])
			if not data6.empty:
				plt.plot_date(data6.last(td).index, data6['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
				plt.text(data6.index[-1:][0], data6['Humidity'][-1], data6['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][6])
				#plt.text(data6.index[-1:][0], data6['Humidity'][-1] + label_offset, sensor6label, fontsize=12, color=plt.rcParams['axes.color_cycle'][6])
			if not data7.empty:
				plt.plot_date(data7.last(td).index, data7['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
				plt.text(data7.index[-1:][0], data7['Humidity'][-1], data7['Humidity'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][7])
			plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
			plt.title('Humidity Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Humid (%)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
			fig.savefig('/home/pi/Power_Monitoring/output/plot_humid.png', bbox_inches='tight')
		if volt_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
			plt.style.use(plot_style)
			plt.rcParams['axes.facecolor']='w'
			if not data0.empty:
				plt.plot_date(data0.last(td).index, data0['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
				plt.text(data0.index[-1:][0], data0['Voltage'][-1], data0['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
				#plt.text(data0.index[-1:][0], data0['Voltage'][-1] + label_offset, sensor0label, fontsize=12, color=plt.rcParams['axes.color_cycle'][0])
			if not data1.empty:
				plt.plot_date(data1.last(td).index, data1['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
				plt.text(data1.index[-1:][0], data1['Voltage'][-1], data1['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][1])
				#plt.text(data1.index[-1:][0], data1['Voltage'][-1] + label_offset, sensor1label, fontsize=12, color=plt.rcParams['axes.color_cycle'][1])
			if not data2.empty:
				plt.plot_date(data2.last(td).index, data2['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
				plt.text(data2.index[-1:][0], data2['Voltage'][-1], data2['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][2])
				#plt.text(data2.index[-1:][0], data2['Voltage'][-1] + label_offset, sensor2label, fontsize=12, color=plt.rcParams['axes.color_cycle'][2])
			if not data3.empty:
				plt.plot_date(data3.last(td).index, data3['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
				plt.text(data3.index[-1:][0], data3['Voltage'][-1], data3['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][3])
				#plt.text(data3.index[-1:][0], data3['Voltage'][-1] + label_offset, sensor3label, fontsize=12, color=plt.rcParams['axes.color_cycle'][3])
			if not data4.empty:
				plt.plot_date(data4.last(td).index, data4['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
				plt.text(data4.index[-1:][0], data4['Voltage'][-1], data4['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][4])
				#plt.text(data4.index[-1:][0], data4['Voltage'][-1] + label_offset, sensor4label, fontsize=12, color=plt.rcParams['axes.color_cycle'][4])
			if not data5.empty:
				plt.plot_date(data5.last(td).index, data5['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
				plt.text(data5.index[-1:][0], data5['Voltage'][-1], data5['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][5])
				#plt.text(data5.index[-1:][0], data5['Voltage'][-1] + label_offset, sensor5label, fontsize=12, color=plt.rcParams['axes.color_cycle'][5])
			if not data6.empty:
				plt.plot_date(data6.last(td).index, data6['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
				plt.text(data6.index[-1:][0], data6['Voltage'][-1], data6['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][6])
				#plt.text(data6.index[-1:][0], data6['Voltage'][-1] + label_offset, sensor6label, fontsize=12, color=plt.rcParams['axes.color_cycle'][6])
			if not data7.empty:
				plt.plot_date(data7.last(td).index, data7['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
				plt.text(data7.index[-1:][0], data7['Voltage'][-1], data7['Voltage'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][7])
			plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
			plt.title('Voltage Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Voltage (%)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
			fig.savefig('/home/pi/Power_Monitoring/output/plot_volt.png', bbox_inches='tight')
		if rssi_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
			plt.style.use(plot_style)
			plt.rcParams['axes.facecolor']='w'
			if not data0.empty:
				plt.plot_date(data0.last(td).index, data0['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
				plt.text(data0.index[-1:][0], data0['RSSI'][-1], data0['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][0])
				#plt.text(data0.index[-1:][0], data0['RSSI'][-1] + label_offset, sensor0label, fontsize=12, color=plt.rcParams['axes.color_cycle'][0])
			if not data1.empty:
				plt.plot_date(data1.last(td).index, data1['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
				plt.text(data1.index[-1:][0], data1['RSSI'][-1], data1['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][1])
				#plt.text(data1.index[-1:][0], data1['RSSI'][-1] + label_offset, sensor1label, fontsize=12, color=plt.rcParams['axes.color_cycle'][1])
			if not data2.empty:
				plt.plot_date(data2.last(td).index, data2['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label=sensor2label)
				plt.text(data2.index[-1:][0], data2['RSSI'][-1], data2['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][2])
				#plt.text(data2.index[-1:][0], data2['RSSI'][-1] + label_offset, sensor2label, fontsize=12, color=plt.rcParams['axes.color_cycle'][2])
			if not data3.empty:
				plt.plot_date(data3.last(td).index, data3['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
				plt.text(data3.index[-1:][0], data3['RSSI'][-1], data3['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][3])
				#plt.text(data3.index[-1:][0], data3['RSSI'][-1] + label_offset, sensor3label, fontsize=12, color=plt.rcParams['axes.color_cycle'][3])
			if not data4.empty:
				plt.plot_date(data4.last(td).index, data4['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
				plt.text(data4.index[-1:][0], data4['RSSI'][-1], data4['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][4])
				#plt.text(data4.index[-1:][0], data4['RSSI'][-1] + label_offset, sensor4label, fontsize=12, color=plt.rcParams['axes.color_cycle'][4])
			if not data5.empty:
				plt.plot_date(data5.last(td).index, data5['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
				plt.text(data5.index[-1:][0], data5['RSSI'][-1], data5['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][5])
				#plt.text(data5.index[-1:][0], data5['RSSI'][-1] + label_offset, sensor5label, fontsize=12, color=plt.rcParams['axes.color_cycle'][5])
			if not data6.empty:
				plt.plot_date(data6.last(td).index, data6['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
				plt.text(data6.index[-1:][0], data6['RSSI'][-1], data6['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][6])
				#plt.text(data6.index[-1:][0], data6['RSSI'][-1] + label_offset, sensor6label, fontsize=12, color=plt.rcParams['axes.color_cycle'][6])
			if not data7.empty:
				plt.plot_date(data7.last(td).index, data7['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', color=plt.rcParams['axes.color_cycle'][7], label=sensor7label)
				plt.text(data7.index[-1:][0], data7['RSSI'][-1], data7['RSSI'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, backgroundcolor='w', color=plt.rcParams['axes.color_cycle'][7])
			plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
			plt.title('RSSI Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Voltage (%)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
			fig.savefig('/home/pi/Power_Monitoring/output/plot_rssi.png', bbox_inches='tight')
	except Exception:
		print("MATPLOTLIB ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)
