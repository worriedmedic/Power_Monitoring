import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time, datetime
import traceback

if (1):
  if (today != datetime.date.today()):
    today = datetime.date.today()
    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    fname = str(today) + '.log'
    fdirectory = 'data_log/' + time.strftime("%Y-%m")

    try:
      data_yest = data_today
      data_yest0 = data_today0
      data_yest1 = data_today1
      data_yest2 = data_today2
      data_yest3 = data_today3
      data_yest4 = data_today4
    except exception:
      print("TODAY TO YESTERDAY DATA XFER")
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)
      
    try:
      data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + time.strftime("%Y-%m") + '/' + str(today) + '.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"])
      data_today['Temperature'] = s['Temperature'].map(lambda x: x.lstrip('T'))
      data_today['Pressure'] = s['Pressure'].map(lambda x: x.lstrip('P'))
      data_today['Humidity'] = s['Humidity'].map(lambda x: x.lstrip('H'))
      data_today['Voltage'] = s['Voltage'].map(lambda x: x.lstrip('V'))

      data_today['Datetime'] = pd.to_datetime(data_today['Date'] + ' ' + data_today['Time'])
      data_today.setindex('Datetime')
      data_today.drop(['Date', 'Time'], 1)

      data_today0 = data_today.loc[s['Address'] == 0]
      data_today1 = data_today.loc[s['Address'] == 1]
      data_today2 = data_today.loc[s['Address'] == 2]
      data_today3 = data_today.loc[s['Address'] == 3]
      data_today4 = data_today.loc[s['Address'] == 4]
      
    except Exception:
      print("READ CSV ERROR")
			traceback.print_exc(file=sys.stdout)
			print('-' * 60)

    try:
      data_today
      data_today0
      data_today1
      data_today2
      data_today3
      data_today4
    except Exception:
      print("READ CSV ERROR")
			traceback.print_exc(file=sys.stdout)
			print('-' * 60) 
