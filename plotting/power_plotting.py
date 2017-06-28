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

location = 'dover'
dropbox_upload = True

today = datetime.date.today()
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
prior2 = datetime.date.today() + datetime.timedelta(days=-2)
prior3 = datetime.date.today() + datetime.timedelta(days=-3)
prior4 = datetime.date.today() + datetime.timedelta(days=-4)
prior5 = datetime.date.today() + datetime.timedelta(days=-5)
prior6 = datetime.date.today() + datetime.timedelta(days=-6)
prior7 = datetime.date.today() + datetime.timedelta(days=-7)

now = datetime.datetime.now()

try:
  data_today = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + today.strftime("%Y-%m") + '/' + str(today) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_today_valid = True
except Exception:
  data_today_valid = False

try:
  data_yesterday = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + yesterday.strftime("%Y-%m") + '/' + str(yesterday) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_yesterday_valid = True
except Exception:
  data_yesterday_valid = False

try:
  data_2prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior2.strftime("%Y-%m") + '/' + str(prior2) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_3prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior3.strftime("%Y-%m") + '/' + str(prior3) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_4prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior4.strftime("%Y-%m") + '/' + str(prior4) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_5prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior5.strftime("%Y-%m") + '/' + str(prior5) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_6prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior6.strftime("%Y-%m") + '/' + str(prior6) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_7prior = pd.read_csv('/home/pi/Power_Monitoring/data_log/' + prior7.strftime("%Y-%m") + '/' + str(prior7) + 'POWER.log', names = ["Date", "Time", "CT1", "CT2", "CT3", "CT4", "VRMS", "Pulse"])
  data_week_valid = True
except Exception:
  data_week_valid = False

if (data_today_valid and data_yesterday_valid and data_week_valid):
  data = pd.concat([data_7prior, data_6prior, data_5prior, data_4prior, data_3prior, data_2prior, data_yesterday, data_today])
elif (data_today_valid and data_yesterday_valid):
  data = pd.concat([data_yesterday, data_today])
elif (data_today_valid):
  data = data_today

data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
data = data.drop(['Date', 'Time'], 1)
data = data.set_index('Datetime')

data['CT1'] = data['CT1'].str.replace('ct1:', '')
data['CT2'] = data['CT2'].str.replace('ct2:', '')
data['CT3'] = data['CT3'].str.replace('ct3:', '')
data['CT4'] = data['CT4'].str.replace('ct4:', '')
data['VRMS'] = data['VRMS'].str.replace('vrms:', '')
data['Pulse'] = data['Pulse'].str.replace('pulse:', '')  
data = data.convert_objects(convert_numeric=True)
data['CTT'] = data['CT1'] + data['CT2']

td1 = '3H'
td2 = '24H'
td3 = '7D'

try:
  fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
  plt.style.use(plot_style)
  plt.rcParams['axes.facecolor']='w'
  plt.plot_date(data.last(td1).index, data['CTT'].last(td1).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][0], label="CTT")
  plt.fill_between(data.last(td1).index, data['CTT'].last(td1).values, facecolor=plt.rcParams['axes.color_cycle'][0], alpha=0.35)
  plt.text(data.index[-1:][0], data['CTT'][-1], data['CTT'][-1], fontsize=8, horizontalalignment='left', verticalalignment='top', rotation=45, color=plt.rcParams['axes.color_cycle'][0])
  plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
  plt.title('Dover Power Usage: %s' %td1)
  plt.xlabel('Time')
  plt.ylabel('Watts')
  plt.grid(False)
  plt.tight_layout()
  myFmt = mdates.DateFormatter('%m-%d %H:%M')
  fig.axes[0].get_xaxis().set_major_formatter(myFmt)
  fig.autofmt_xdate()
  fig.text(0.5, 0.5, 'Dover Power Monitoring', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
  fig.savefig('/home/pi/Power_Monitoring/output/%spower.png' %td1, bbox_inches='tight')
  subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/%spower.png" %td1])
  subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/%spower.png" %td1, "/var/www/html/"])
  if dropbox_upload:
    subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/output/%spower.png" %td1, "/Programming/logs/%s/plots/" %location])
except Exception:
  print "%s Error" %td1
  traceback.print_exc(file=sys.stdout)

try:
  fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
  plt.style.use(plot_style)
  plt.rcParams['axes.facecolor']='w'
  plt.plot_date(data.last(td2).index, data['CTT'].last(td2).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][1], label="CTT")
  plt.fill_between(data.last(td2).index, data['CTT'].last(td2).values, facecolor=plt.rcParams['axes.color_cycle'][1], alpha=0.35)
  plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
  plt.title('Dover Power Usage: %s' %td2)
  plt.xlabel('Time')
  plt.ylabel('Watts')
  plt.grid(False)
  plt.tight_layout()
  myFmt = mdates.DateFormatter('%m-%d %H:%M')
  fig.axes[0].get_xaxis().set_major_formatter(myFmt)
  fig.autofmt_xdate()
  fig.text(0.5, 0.5, 'Dover Power Monitoring', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
  fig.savefig('/home/pi/Power_Monitoring/output/%spower.png' %td2, bbox_inches='tight')
  subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/%spower.png" %td2])
  subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/%spower.png" %td2, "/var/www/html/"])
  if dropbox_upload:
    subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/output/%spower.png" %td2, "/Programming/logs/%s/plots/" %location])
except Exception:
  print "%s Error" %td2
  traceback.print_exc(file=sys.stdout)

try:
  fig = plt.figure(figsize=(plt_size_x, plt_size_y), dpi=plt_size_dpi)
  plt.style.use(plot_style)
  plt.rcParams['axes.facecolor']='w'
  plt.plot_date(data.last(td3).index, data['CTT'].last(td3).values, linestyle="solid", linewidth=line_width, marker='None', color=plt.rcParams['axes.color_cycle'][2], label="CTT")
  plt.fill_between(data.last(td3).index, data['CTT'].last(td3).values, facecolor=plt.rcParams['axes.color_cycle'][2], alpha=0.35)
  plt.legend(loc=2, ncol=2, fontsize=8).set_visible(True)
  plt.title('Dover Power Usage: %s' %td3)
  plt.xlabel('Time')
  plt.ylabel('Watts')
  plt.grid(False)
  plt.tight_layout()
  myFmt = mdates.DateFormatter('%m-%d')
  fig.axes[0].get_xaxis().set_major_formatter(myFmt)
  fig.autofmt_xdate()
  fig.text(0.5, 0.5, 'Dover Power Monitoring', fontsize=25, color='gray', ha='center', va='center', alpha=0.35)
  fig.savefig('/home/pi/Power_Monitoring/output/%spower.png' %td3, bbox_inches='tight')
  subprocess.call(["sudo", "chmod", "+x", "/home/pi/Power_Monitoring/output/%spower.png" %td3])
  subprocess.call(["sudo", "cp", "/home/pi/Power_Monitoring/output/%spower.png" %td3, "/var/www/html/"])
  if dropbox_upload:
    subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "/home/pi/Power_Monitoring/output/%spower.png" %td3, "/Programming/logs/%s/plots/" %location])
except Exception:
  print "%s Error" %td3
  traceback.print_exc(file=sys.stdout)
