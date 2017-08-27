#/bin/python
import datetime, time
from gpiozero import CPUTemperature
import matplotlib.pyplot as plt

plt.ion()
x = []
y = []

def datawrite(temp):
	with open("/home/pi/Power_Monitoring/data_log/cpu_temp.csv", "a") as log:
		log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

def graph(temp):
	y.append(temp)
	x.append(time.time ())
	plt.clf()
	plt.scatter(x,y)
	plt.plot(x,y)
	plt.draw() 

running = True
while running:
	temp = CPUTemperature()
	datawrite(temp)
	#graph(temp)
	time.sleep(10)
