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
			fig = plt.figure(figsize=(7.5, 10))

			plt.style.use('grayscale')

			plt.plot_date(data0.last('16H').index, data0['Temperature'].last('16H').values, linestyle="solid", linewidth=2, marker='None', color='0', label="Sensor 00")
			plt.plot_date(data1.last('16H').index, data1['Temperature'].last('16H').values, linestyle="dashed", linewidth=2, marker='None', color='0.45', label="Sensor 01")
			plt.plot_date(data2.last('16H').index, data2['Temperature'].last('16H').values, linestyle="dashdot", linewidth=2, marker='None', color='0.3', label="Sensor 02")
			plt.plot_date(data4.last('16H').index, data4['Temperature'].last('16H').values, linestyle="dotted", linewidth=2, marker='None', color='0', label="Sensor 04")
			plt.legend(loc=0)
			plt.title('Temperature Plot: Past 16 Hours')
			plt.xlabel('Time')
			plt.ylabel('Temp (F)')
			plt.grid()
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_temp.png', bbox_inches='tight')
		
		if press_plot:
			fig = plt.figure(figsize=(7.5, 10))

			plt.style.use('grayscale')

			plt.plot_date(data0.last('16H').index, data0['Pressure'].last('16H').values, linestyle="solid", linewidth=2, marker='None', color='0', label="Sensor 00")
			plt.plot_date(data1.last('16H').index, data1['Pressure'].last('16H').values, linestyle="dashed", linewidth=2, marker='None', color='0.45', label="Sensor 01")
			plt.plot_date(data2.last('16H').index, data2['Pressure'].last('16H').values, linestyle="dashdot", linewidth=2, marker='None', color='0.3', label="Sensor 02")
			plt.plot_date(data4.last('16H').index, data4['Pressure'].last('16H').values, linestyle="dotted", linewidth=2, marker='None', color='0', label="Sensor 04")
			plt.legend(loc=0)
			plt.title('Pressure Plot: Past 16 Hours')
			plt.xlabel('Time')
			plt.ylabel('Pressure (hPa)')
			plt.grid()
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_press.png', bbox_inches='tight')
			
		if humid_plot:
			fig = plt.figure(figsize=(7.5, 10))

			plt.style.use('grayscale')

			plt.plot_date(data0.last('16H').index, data0['Humidity'].last('16H').values, linestyle="solid", linewidth=2, marker='None', color='0', label="Sensor 00")
			plt.plot_date(data1.last('16H').index, data1['Humidity'].last('16H').values, linestyle="dashed", linewidth=2, marker='None', color='0.45', label="Sensor 01")
			plt.plot_date(data2.last('16H').index, data2['Humidity'].last('16H').values, linestyle="dashdot", linewidth=2, marker='None', color='0.3', label="Sensor 02")
			plt.plot_date(data4.last('16H').index, data4['Humidity'].last('16H').values, linestyle="dotted", linewidth=2, marker='None', color='0', label="Sensor 04")
			plt.legend(loc=0)
			plt.title('Humidity Plot: Past 16 Hours')
			plt.xlabel('Time')
			plt.ylabel('Humid (%)')
			plt.grid()
			plt.tight_layout()
			fig.autofmt_xdate()
			fig.savefig('/home/pi/Power_Monitoring/output/plot_humid.png', bbox_inches='tight')
			
	except Exception:
		print("MATPLOTLIB ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60) 
