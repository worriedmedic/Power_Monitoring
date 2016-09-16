import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys, os.path

temp_plot = True
press_plot = True
humid_plot = True

td = '16H'

line_width = 4
marker_size = 6

face_color = 'white'

if os.path.isfile('/home/pi/Power_Monitoring/dover.location'):
	plt_size_x   = 10
	plt_size_y   = 8
	plt_size_dpi = 100
	plot_style   = 'bmh' 
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
elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
	plt_size_x   = 6.5
	plt_size_y   = 9
	plt_size_dpi = 84
	plot_style   = 'grayscale'
	sensor0      = '00'
	sensor0label = 'Outside'
	sensor1      = '01'
	sensor1label = 'Upstairs'
	sensor2      = None # Dead as per LWH 09-16-2016
	sensor2label = None
	sensor3      = '03'
	sensor3label = 'Barn Upstairs'
	sensor4      = '04'
	sensor4label = 'Reeds Room'


if (1):
	today = datetime.date.today()
	yesterday = datetime.date.today() + datetime.timedelta(days=-1)
	now = datetime.datetime.now()
	now_minus_eight = now + datetime.timedelta(hours=-8)
	
	try:
		data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m") + '/' + str(yesterday) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		
		data = pd.concat([data_yest, data_today])
		
		data['Temperature'] = data['Temperature'].str.replace('T', '')
		data['Pressure'] = data['Pressure'].str.replace('P', '')
		data['Humidity'] = data['Humidity'].str.replace('H', '')
		data['Voltage'] = data['Voltage'].str.replace('V', '')
		
		data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
		
		data = data.drop(['Date', 'Time'], 1)
		data = data.set_index('Datetime')
		
		data0 = data.loc[data['Address'] == sensor0]
		data1 = data.loc[data['Address'] == sensor1]
		data2 = data.loc[data['Address'] == sensor2]
		data3 = data.loc[data['Address'] == sensor3]
		data4 = data.loc[data['Address'] == sensor4]

	except Exception:
		print("TODAY READ CSV ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

	try:
		if temp_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi, facecolor=face_color)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data4.last(td).index, data4['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.legend(loc=0)
			plt.title('Temperature Plot: Past 16 Hours')
			plt.xlabel('Time')
			plt.ylabel('Temp (F)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_temp_16.png', bbox_inches='tight')
		
		if press_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi, facecolor=face_color)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data4.last(td).index, data4['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.legend(loc=0)
			plt.title('Pressure Plot: Past 16 Hours')
			plt.xlabel('Time')
			plt.ylabel('Pressure (hPa)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_press_16.png', bbox_inches='tight')
			
		if humid_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi, facecolor=face_color)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data4.last(td).index, data4['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.legend(loc=0)
			plt.title('Humidity Plot: Past 16 Hours')
			plt.xlabel('Time')
			plt.ylabel('Humid (%)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_humid_16.png', bbox_inches='tight')
			
	except Exception:
		print("MATPLOTLIB ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60) 
