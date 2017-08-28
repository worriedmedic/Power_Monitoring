#/bin/python
#temperature plotting from ~/Power_Monitoring/data_log/cpu_temp.csv

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time, datetime
import traceback
import sys, os.path
import subprocess

plt_size_x   = 10
plt_size_y   = 8
plt_size_dpi = 100
plot_style   = 'bmh'
line_width = 0.5
rssi_line_width = 1
label_offset = 3
td = '3D'

def readdata():
	global data
	data = pd.read_csv('/home/pi/Power_Monitoring/data_log/cpu_temp.csv', names = ["Datetime", "Temperature"])
	data['Datetime'] = pd.to_datetime(data['Datetime'])
	data = data.set_index('Datetime')

def plotdata():
	fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
	plt.style.use(plot_style)
	plt.rcParams['axes.facecolor']='w'
	plt.plot_date(data.last(td).index, data['Temperature'].last(td).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label="Temp")
	plt.title('CPU Temperature: %s' %td)
	plt.xlabel('Time')
	plt.ylabel('Temperature (C)')
	plt.tight_layout()
	myFmt = mdates.DateFormatter('%m-%d %H:%M')
	fig.axes[0].get_xaxis().set_major_formatter(myFmt)
	fig.autofmt_xdate()
	fig.text(0.5, 0.5, 'Cuttyhunk Wx St', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
	fig.savefig('/home/pi/Power_Monitoring/output/cpu_temp.png', bbox_inches='tight')
	subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/cpu_temp.png"])
	subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/cpu_temp.png", "/var/www/html/"])

if (1):
	try:
		readdata()
		plotdata()
	except Exception:
		print("ERROR")
		traceback.print_exc(file=sys.stdout)
	
