import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys

temp_plot = True
press_plot = True
humid_plot = True

if (1):
	today = datetime.date.today()
	yesterday = datetime.date.today() + datetime.timedelta(days=-1)
	now = time.strftime("%H:%M")
	now_minus_eight = '{:%H:%M}'.format(datetime.datetime.now() + datetime.timedelta(hours=-8))
	
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
		
		data0 = data.loc[data['Address'] == '00']
		data1 = data.loc[data['Address'] == '01']
		data2 = data.loc[data['Address'] == '02']
		data3 = data.loc[data['Address'] == '03']
		data4 = data.loc[data['Address'] == '04']

	except Exception:
		print("TODAY READ CSV ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

	try:
		if temp_plot:
			fig = plt.figure(figsize=(6, 8))

			plt.style.use('fivethirtyeight')

			plt.plot_date(data0.between_time(now_minus_eight, now).index, data0['Temperature'].between_time(now_minus_eight, now).values, label="Sensor 00")
			plt.plot_date(data1.between_time(now_minus_eight, now).index, data1['Temperature'].between_time(now_minus_eight, now).values, label="Sensor 01")
			plt.plot_date(data2.between_time(now_minus_eight, now).index, data2['Temperature'].between_time(now_minus_eight, now).values, label="Sensor 02")
			plt.plot_date(data4.between_time(now_minus_eight, now).index, data4['Temperature'].between_time(now_minus_eight, now).values, label="Sensor 04")
			plt.legend(loc=0)
			plt.title('Temperature Plot: Past 8 Hours')
			plt.xlabel('Time')
			plt.ylabel('Temp (F)')
			plt.grid()
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_temp.png', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
		
		if press_plot:
			fig = plt.figure(figsize=(6, 8))

			plt.style.use('fivethirtyeight')

			plt.plot_date(data0.between_time(now_minus_eight, now).index, data0['Pressure'].between_time(now_minus_eight, now).values, label="Sensor 00")
			plt.plot_date(data1.between_time(now_minus_eight, now).index, data1['Pressure'].between_time(now_minus_eight, now).values, label="Sensor 01")
			plt.plot_date(data2.between_time(now_minus_eight, now).index, data2['Pressure'].between_time(now_minus_eight, now).values, label="Sensor 02")
			plt.plot_date(data4.between_time(now_minus_eight, now).index, data4['Pressure'].between_time(now_minus_eight, now).values, label="Sensor 04")
			plt.legend(loc=0)
			plt.title('Pressure Plot: Past 8 Hours')
			plt.xlabel('Time')
			plt.ylabel('Pressure (hPa)')
			plt.grid()
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_press.png', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
			
		if humid_plot:
			fig = plt.figure(figsize=(6, 8))

			plt.style.use('fivethirtyeight')

			plt.plot_date(data0.between_time(now_minus_eight, now).index, data0['Humidity'].between_time(now_minus_eight, now).values, label="Sensor 00")
			plt.plot_date(data1.between_time(now_minus_eight, now).index, data1['Humidity'].between_time(now_minus_eight, now).values, label="Sensor 01")
			plt.plot_date(data2.between_time(now_minus_eight, now).index, data2['Humidity'].between_time(now_minus_eight, now).values, label="Sensor 02")
			plt.plot_date(data4.between_time(now_minus_eight, now).index, data4['Humidity'].between_time(now_minus_eight, now).values, label="Sensor 04")
			plt.legend(loc=0)
			plt.title('Pressure Plot: Past 8 Hours')
			plt.xlabel('Time')
			plt.ylabel('Humid (%)')
			plt.grid()
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_press.png', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
			
	except Exception:
		print("MATPLOTLIB ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60) 
