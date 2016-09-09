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

plot = plt.plot(s0['Time'].values, s0['Temperature'].values)
fig = plot.get_figure()
fig.savefig("output.png")
