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
volt_plot = True
rssi_plot = True

######## GLOBAL VAR #######
td = '48H'
line_width = 3
rssi_line_width = 1.5

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
	sensor2label = 'MBedroom'
	sensor3      = '06'
	sensor3label = 'Garage'
	sensor4      = '05'
	sensor4label = 'Guest'
	sensor5      = '04'
	sensor5label = 'Downstairs'
	sensor6	     = '03'
	sensor6label = 'Laundry'
elif os.path.isfile('/home/pi/Power_Monitoring/cuttyhunk.location'):
	plt_size_x   = 6.5
	plt_size_y   = 9
	plt_size_dpi = 84
	plot_style   = 'grayscale'
	sensor0      = '00'
	sensor0label = 'Outside'
	sensor1      = '01'
	sensor1label = 'Upstairs'
	sensor2      = '04' 
	sensor2label = 'Reeds Room'
	sensor3      = None # '02' Dead as per LWH 09-16-2016
	sensor3label = None # 'Barn Upstairs'
	sensor4      = None # '03' Dead as per LWH 09-22-2016
	sensor4label = None # 'Downstairs'


if (1):
	today = datetime.date.today()
	yesterday = datetime.date.today() + datetime.timedelta(days=-1)
	prior2 = datetime.date.today() + datetime.timedelta(days=-2)
	prior3 = datetime.date.today() + datetime.timedelta(days=-3)
	
	now = datetime.datetime.now()
	now_minus_eight = now + datetime.timedelta(hours=-8)
	
	try:
		data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + yesterday.strftime("%Y-%m") + '/' + str(yesterday) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior2.strftime("%Y-%m") + '/' + str(prior2) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		
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
		data5 = data.loc[data['Address'] == sensor5]
		data6 = data.loc[data['Address'] == sensor6]
		
	except Exception:
		print("TODAY READ CSV ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

	try:
		if temp_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data3.last(td).index, data3['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor3label)
			plt.plot_date(data4.last(td).index, data4['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.plot_date(data5.last(td).index, data5['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor5label)
			plt.plot_date(data6.last(td).index, data6['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor6label)
			plt.legend(loc=0)
			plt.title('Temperature Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Temp (F)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_temp.png', bbox_inches='tight')
		
		if press_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data3.last(td).index, data3['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor3label)
			plt.plot_date(data4.last(td).index, data4['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.plot_date(data5.last(td).index, data5['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor5label)
			plt.plot_date(data6.last(td).index, data6['Pressure'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor6label)
			plt.legend(loc=0)
			plt.title('Pressure Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Pressure (hPa)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_press.png', bbox_inches='tight')
			
		if humid_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data3.last(td).index, data3['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor3label)
			plt.plot_date(data4.last(td).index, data4['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.plot_date(data5.last(td).index, data5['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor5label)
			plt.plot_date(data6.last(td).index, data6['Humidity'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor6label)
			plt.legend(loc=0)
			plt.title('Humidity Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Humid (%)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_humid.png', bbox_inches='tight')
		
		if volt_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor2label)
			plt.plot_date(data3.last(td).index, data3['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor3label)
			plt.plot_date(data4.last(td).index, data4['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor4label)
			plt.plot_date(data5.last(td).index, data5['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor5label)
			plt.plot_date(data6.last(td).index, data6['Voltage'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', label=sensor6label)
			plt.legend(loc=0)
			plt.title('Voltage Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('Voltage (%)')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_volt.png', bbox_inches='tight')

		if rssi_plot:
			fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)

			plt.style.use(plot_style)

			plt.plot_date(data0.last(td).index, data0['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor0label)
			plt.plot_date(data1.last(td).index, data1['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor1label)
			plt.plot_date(data2.last(td).index, data2['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor2label)
			plt.plot_date(data3.last(td).index, data3['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor3label)
			plt.plot_date(data4.last(td).index, data4['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor4label)
			plt.plot_date(data5.last(td).index, data5['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor5label)
			plt.plot_date(data6.last(td).index, data6['RSSI'].last(td).values, linestyle="solid", linewidth=rssi_line_width, marker='None', label=sensor6label)
			plt.legend(loc=0)
			plt.title('RSSI Plot: Past %s' %td)
			plt.xlabel('Time')
			plt.ylabel('RSSI')
			plt.grid(True)
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_rssi.png', bbox_inches='tight')
			
	except Exception:
		print("MATPLOTLIB ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60) 
