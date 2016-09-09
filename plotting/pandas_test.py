import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

s = pd.read_csv('/home/pi/Power_Monitoring/data_log/2016-09/2016-09-09.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"])
s['Temperature'] = s['Temperature'].map(lambda x: x.lstrip('T'))
s['Pressure'] = s['Pressure'].map(lambda x: x.lstrip('P'))
s['Humidity'] = s['Humidity'].map(lambda x: x.lstrip('H'))
s['Voltage'] = s['Voltage'].map(lambda x: x.lstrip('V'))

s = s.drop('Date', 1)
s['Time'] = pd.to_datetime(s['Time'])

s0 = s.loc[s['Address'] == 0]
s1 = s.loc[s['Address'] == 1]
s2 = s.loc[s['Address'] == 2]
s3 = s.loc[s['Address'] == 3]
s4 = s.loc[s['Address'] == 4]

plt.figure()

#dates = matplotlib.dates.date2num(s0['Time'])
#plot_date(dates, values)

fig, ax1 = plt.subplot(211)
ax1 = plt.plot_date(s0['Time'], s0['Temperature'].values.astype(float))
ax1.setp(ax1, color='r', linewidth=2.0)
ax1.title('Ext Sensor: Temp')
ax1.xlabel('Time')
ax1.ylabel('Temp')

fig, ax2 = plt.subplot(212)
ax2 = plot_dates(s0['Time'], s0['Pressure'].values.astype(float))
ax2.setp(ax2, color='r', linewidth=2.0)
ax2.xlabel('Time')
ax2.ylabel('Press')


plt.savefig("output.png")
plt.show()
