import pandas as pd
import os
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time, datetime
import traceback

location = 'cuttyhunk'
sensor0		= 93
sensor0label	= 'Outside'
sensor1		= 96
sensor1label	= 'Upstairs'
sensor2		= 99
sensor2label	= 'Upstairs 2'
sensor3		= 95
sensor3label	= 'Reeds Room'
sensor4		= 98
sensor4label	= 'Utility Room'
sensor5		= 97
sensor5label	= 'Barn'
sensor6		= 94
sensor6label	= 'Paint Shed'
sensor7		= 90
sensor7label	= 'None'

#timedelta    = '6M'
plt_size_x   = 60
plt_size_y   = 20
plt_size_dpi = 100
plot_style   = 'bmh'
line_width = 1.5
rssi_line_width = 1
label_offset = 3

data = []
months = ['05', '06', '07', '08', '09', '10']
allfiles = []
list_ = []

for month_ in months:
	path = '/Users/lantz/Dropbox/Programming/logs/cuttyhunk/2017-%s/' %month_
	files_ = glob.glob(path + "*.log")
	allfiles.extend(files_)

for file in allfiles:
	data = pd.read_csv(file, names = ["Date", "Time", "Address", "Temperature", "Pressure", "Humidity", "Voltage", "RSSI"], dtype=str)
	list_.append(data)

data = pd.concat(list_)
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
data = data.drop(['Date', 'Time'], 1)
data = data.set_index('Datetime')
data['Temperature'] = data['Temperature'].str.replace('T', '')
data['Pressure'] = data['Pressure'].str.replace('P', '')
data['Humidity'] = data['Humidity'].str.replace('H', '')
data['Voltage'] = data['Voltage'].str.replace('V', '')
data = data.convert_objects(convert_numeric=True)
data['Dewpoint'] = data['Temperature'].values - (0.36 * (100 - data['Humidity'].values))

data0 = data.loc[data['Address'] == sensor0]
data1 = data.loc[data['Address'] == sensor1]
data2 = data.loc[data['Address'] == sensor2]
data3 = data.loc[data['Address'] == sensor3]
data4 = data.loc[data['Address'] == sensor4]
data5 = data.loc[data['Address'] == sensor5]
data6 = data.loc[data['Address'] == sensor6]
data7 = data.loc[data['Address'] == sensor7]

def dataplot(datatype):
	fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
	plt.rcParams['axes.facecolor']='w'
	plt.plot_date(data0.last('6M').index, data0[datatype].last('6M').values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label=sensor0label)
	plt.plot_date(data1.last('6M').index, data1[datatype].last('6M').values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label=sensor1label)
	plt.plot_date(data3.last('6M').index, data3[datatype].last('6M').values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][3], label=sensor3label)
	plt.plot_date(data4.last('6M').index, data4[datatype].last('6M').values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][4], label=sensor4label)
	plt.plot_date(data5.last('6M').index, data5[datatype].last('6M').values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][5], label=sensor5label)
	plt.plot_date(data6.last('6M').index, data6[datatype].last('6M').values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][6], label=sensor6label)
	plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
	plt.title('2017 Cuttyhunk %s Plots' %datatype)
	plt.xlabel('Time')
	plt.ylabel('%s' %datatype)
	plt.grid(True)
	plt.tight_layout()
	myFmt = mdates.DateFormatter('%m-%d')
	fig.axes[0].get_xaxis().set_major_formatter(myFmt)
	#fig.autofmt_xdate()
	fig.text(0.5, 0.5, '%s Weather Station' %location, fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
	fig.savefig("2017_Cuttyhunk_%s.png" %datatype)


dataplot('Temperature')
dataplot('Pressure')
dataplot('Voltage')
