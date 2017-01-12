import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time, datetime
import traceback
import sys, os.path

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
