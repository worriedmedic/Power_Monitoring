import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s = pd.read_csv('/home/pi/Power_Monitoring/data_log/2016-09/2016-09-09.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"])
s['Temperature'] = s['Temperature'].map(lambda x: x.lstrip('T'))
s['Pressure'] = s['Pressure'].map(lambda x: x.lstrip('P'))
s['Humidity'] = s['Humidity'].map(lambda x: x.lstrip('H'))
s['Voltage'] = s['Voltage'].map(lambda x: x.lstrip('V'))

#s = s.drop('Date', 1)

s0 = s.loc[s['Address'] == 0]
s1 = s.loc[s['Address'] == 1]
s2 = s.loc[s['Address'] == 2]
s3 = s.loc[s['Address'] == 3]
s4 = s.loc[s['Address'] == 4]

fig = plt.figure()

ax1 = fig.add_subplot(211)
plt.plot(pd.to_datetime(s0['Time']), s0['Temperature'].values.astype(float))
plt.setp(lines, color='r', linewidth=2.0)
plt.title('Ext Sensor: Temp')
plt.xlabel('Time')
plt.ylabel('Temp')
plt.axis('scaled')

ax2 = fig.add_subplot(212, sharex=ax1, sharey=ax1)

#plt.axis([0,12,60,100])
plt.subplot(222, sharex=ax1, sharey=ax1)
plt.plot(pd.to_datetime(s0['Time']), s0['Pressure'].values.astype(float))
plt.setp(lines, color='r', linewidth=2.0)
plt.xlabel('Time')
plt.ylabel('Temp')
plt.axis('scaled')


plt.savefig("output.png")
plt.show()
