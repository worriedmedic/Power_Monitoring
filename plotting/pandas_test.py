import time
import datetime
import requests
import os.path
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

##  Plotting function
##
##  The goal of this is to dynamically take the logs of prior data and display them on a graph or in a table.
##  The timing is up to change and can be altered right after this line. The integer will represent the number of hours to look back.

prior_time_interval = 4

##  The graphs will display a highlight of the important weather stations.
##  They will cycle through on a interval and will be displayed on the kindle.


try:
    # Assumptions. Directory exists, file exists, file has actual data.
    now = time.strftime("%H:%M:%S") 
    today = datetime.date.today()
    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    fname = str(today) + '.log'
    fdirectory = 'data_log/' + time.strftime("%Y-%m")+'/'
    ## Assuming that this function will be placed in the 'main' dir.	
except Exception:
    print("LOG UPD ERR", str(today), now)
    traceback.print_exc(file=sys.stdout)
    print('-' * 60)

yest = pd.read_csv('/home/pi/Power_Monitoring/'+fdirectory+str(yesterday)+'.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"])
s = pd.read_csv('/home/pi/Power_Monitoring/'+fdirectory+str(today)+'.log', names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"])
s['Temperature'] = s['Temperature'].map(lambda x: x.lstrip('T'))
s['Pressure'] = s['Pressure'].map(lambda x: x.lstrip('P'))
s['Humidity'] = s['Humidity'].map(lambda x: x.lstrip('H'))
s['Voltage'] = s['Voltage'].map(lambda x: x.lstrip('V'))

yest['Temperature'] = yest['Temperature'].map(lambda x: x.lstrip('T'))
yest['Pressure'] = yest['Pressure'].map(lambda x: x.lstrip('P'))
yest['Humidity'] = yest['Humidity'].map(lambda x: x.lstrip('H'))
yest['Voltage'] = yest['Voltage'].map(lambda x: x.lstrip('V'))

#s = s.drop('Date', 1)

s0 = s.loc[s['Address'] == 0]
s1 = s.loc[s['Address'] == 1]
s2 = s.loc[s['Address'] == 2]
s3 = s.loc[s['Address'] == 3]
s4 = s.loc[s['Address'] == 4]

yest0 = yest.loc[yest['Address'] == 0]
yest1 = yest.loc[yest['Address'] == 1]
yest2 = yest.loc[yest['Address'] == 2]
yest3 = yest.loc[yest['Address'] == 3]
yest4 = yest.loc[yest['Address'] == 4]

plt.figure()

dates = matplotlib.dates.date2num(s0['Time'])
#plot_date(dates, values)

plt.subplot(211)
s0temp = plt.plot(dates, s0['Temperature'].values.astype(float))
plt.gcf().autofmt_xdate()
#s0temp = plt.plot_date(dates, s0['Temperature'].values.astype(float))
plt.setp(s0temp, color='r', linewidth=2.0)
plt.title('Ext Sensor: Temp')
plt.xlabel('Time')
plt.ylabel('Temp')

plt.subplot(212)
s0press = plt.plot(dates, s0['Pressure'].values.astype(float))
plt.gcf().autofmt_xdate()
#s0press = plt.plot_date(dates, s0['Pressure'].values.astype(float))
plt.setp(s0press, color='r', linewidth=2.0)
plt.xlabel('Time')
plt.ylabel('Press')


plt.savefig("output.png")
plt.show()
