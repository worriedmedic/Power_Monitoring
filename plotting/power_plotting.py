import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys, os.path

plt_size_x   = 10
plt_size_y   = 8
plt_size_dpi = 100
plot_style   = 'bmh'
td = '48H'
line_width = 2
rssi_line_width = 1
label_offset = 3

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

data = data.astype(float)

data['CTT'] = data['CT1'] + data['CT2']

fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
plt.style.use(plot_style)
plt.rcParams['axes.facecolor']='w'

plt.plot_date(data.last(td).index, data['CTT'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label="CTT")
plt.plot_date(data.last(td).index, data['CT1'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label="CT1")
plt.plot_date(data.last(td).index, data['CT2'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label="CT2")

plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
plt.title('Dover Power Usage: %s' %td)
plt.xlabel('Time')
plt.ylabel('Watts')
plt.grid(True)
plt.tight_layout()
fig.autofmt_xdate()
fig.text(0.5, 0.5, 'Dover Power Monitoring', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
fig.savefig('/home/pi/Power_Monitoring/output/power.png', bbox_inches='tight')
