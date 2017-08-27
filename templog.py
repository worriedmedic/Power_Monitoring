#/bin/python
import datetime, time,
from gpiozero import CPUTemperature
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()
from standards import *


line_width = 1.5
rssi_line_width = 1
label_offset = 3
running = True

def datawrite(temp):
	with open("/home/pi/Power_Monitoring/data_log/cpu_temp.csv", "a") as log:
		log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

def graph():
	y.append(temp)
	x.append(time())
	plt.clf()
	plt.scatter(x,y)
	plt.plot(x,y)
	plt.draw() 

while running:
	temp = CPUTemperature()
	datawrite(temp)
	graph(temp)
	sleep(10)
