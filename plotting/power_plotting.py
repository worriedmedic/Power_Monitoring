import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys, os.path

today = datetime.date.today()
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
prior2 = datetime.date.today() + datetime.timedelta(days=-2)
prior3 = datetime.date.today() + datetime.timedelta(days=-3)
prior4 = datetime.date.today() + datetime.timedelta(days=-4)
prior5 = datetime.date.today() + datetime.timedelta(days=-5)
prior6 = datetime.date.today() + datetime.timedelta(days=-6)
prior7 = datetime.date.today() + datetime.timedelta(days=-7)

now = datetime.datetime.now()

data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_yesterday = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + yesterday.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior2.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_3prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior3.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_4prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior4.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_5prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior5.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_6prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior6.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
data_7prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior7.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])

data = pd.concat([data_7prior, data_6prior, data_5prior, data_4prior, data_3prior, data_2prior, data_yesterday, data_today])
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
data = data.drop(['Date', 'Time'], 1)
data = data.set_index('Datetime')

data['CT1'] = data['CT1'].str.replace('ct1:', '')
data['CT2'] = data['CT2'].str.replace('ct2:', '')
data['CT3'] = data['CT3'].str.replace('ct3:', '')
data['CT4'] = data['CT4'].str.replace('ct4:', '')
data['VRMS'] = data['VRMS'].str.replace('vrms:', '')
data['Pulse'] = data['Pulse'].str.replace('pulse:', '')

