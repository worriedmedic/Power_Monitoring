import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys

if (1):
	today = datetime.date.today()
	yesterday = datetime.date.today() + datetime.timedelta(days=-1)
	now = time.strftime("%H:%M")
	now_minus_eight = '{:%H:%M}'.format(datetime.datetime.now() + datetime.timedelta(hours=-8))
	
	try:
		data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_today['Temperature'] = data_today['Temperature'].str.replace('T', '')
		data_today['Pressure'] = data_today['Pressure'].str.replace('P', '')
		data_today['Humidity'] = data_today['Humidity'].str.replace('H', '')
		data_today['Voltage'] = data_today['Voltage'].str.replace('V', '')
		data_today['Datetime'] = pd.to_datetime(data_today['Date'] + ' ' + data_today['Time'])

		data_today = data_today.drop(['Date', 'Time'], 1)
		data_today = data_today.set_index('Datetime')

		data_today0 = data_today.loc[data_today['Address'] == '00']
		data_today1 = data_today.loc[data_today['Address'] == '01']
		data_today2 = data_today.loc[data_today['Address'] == '02']
		data_today3 = data_today.loc[data_today['Address'] == '03']
		data_today4 = data_today.loc[data_today['Address'] == '04']

	except Exception:
		print("TODAY READ CSV ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

	try:
		data_yest = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m") + '/' + str(yesterday) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
		data_yest['Temperature'] = data_yest['Temperature'].str.replace('T', '')
		data_yest['Pressure'] = data_yest['Pressure'].str.replace('P', '')
		data_yest['Humidity'] = data_yest['Humidity'].str.replace('H', '')
		data_yest['Voltage'] = data_yest['Voltage'].str.replace('V', '')
		data_yest['Datetime'] = pd.to_datetime(data_yest['Date'] + ' ' + data_yest['Time'])

		data_yest = data_yest.drop(['Date', 'Time'], 1)
		data_yest = data_yest.set_index('Datetime')

		data_yest0 = data_yest.loc[data_yest['Address'] == '00']
		data_yest1 = data_yest.loc[data_yest['Address'] == '01']
		data_yest2 = data_yest.loc[data_yest['Address'] == '02']
		data_yest3 = data_yest.loc[data_yest['Address'] == '03']
		data_yest4 = data_yest.loc[data_yest['Address'] == '04']

	except Exception:
		print("YESTERDAY READ CSV ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60)

	try:
		print(data_today0.between_time(now_minus_eight, now))
		#print(data_yest4.between_time('12:00','23:59'))

	except Exception:
		print("PRINT DATA ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60) 

	try:
		fig = plt.figure(figsize=(6, 8))

		plt.style.use('fivethirtyeight')

		plt.plot_date(data_today0.between_time(now_minus_eight, now).index, data_today0['Temperature'].between_time(now_minus_eight, now).values, linestyle="solid", marker='.', label="Sensor 00")
		plt.plot_date(data_today1.between_time(now_minus_eight, now).index, data_today1['Temperature'].between_time(now_minus_eight, now).values, linestyle="solid", marker='.', label="Sensor 01")
		plt.legend(loc=4)
		plt.title('Ext Sensor: Temp')
		plt.xlabel('Time')
		plt.ylabel('Temp')
		plt.grid()
		plt.tight_layout()
		fig.autofmt_xdate()
		fig.savefig('00_01_Temp.png', bbox_inches='tight')
		#plt.show()
	except Exception:
		print("MATPLOTLIB ERROR")
		traceback.print_exc(file=sys.stdout)
		print('-' * 60) 
