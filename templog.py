#/bin/python
import datetime, time
from gpiozero import CPUTemperature

def datawrite(temp):
	with open("/home/pi/Power_Monitoring/data_log/cpu_temp.csv", "a") as log:
		log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp).split('=',1)[1][:5]))

running = True
while running:
	temp = CPUTemperature()
	datawrite(temp)
	time.sleep(10)
