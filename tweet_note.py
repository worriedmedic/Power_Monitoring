import time
from twitter_creds import *
import tweepy
import threading

gatewaylog = '/home/pi/Power_Monitoring/data_log/Gateway_Logger.log'
dataprocesslog = '/home/pi/Power_Monitoring/data_log/Data_to_SVG.log'
plottinglog = '/home/pi/Power_Monitoring/data_log/Matplotlib-plot.log'

api_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def follow(thefile):
	thefile.seek(0,2) # Go to the end of the file
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1) # Sleep briefly
			continue
		yield line


def logfollower(filepath):
	logfile = open(filepath)
	loglines = follow(logfile)
	for line in loglines:
		print line
		try:
			if line != '\n':
      				api.update_status(line)
		except tweepy.TweepError as e:
			print(e.reason)

tgateway = threading.Thread(target=logfollower, args=(gatewaylog,))
tdataproc = threading.Thread(target=logfollower, args=(dataprocesslog,))
tplotting = threading.Thread(target=logfollower, args=(plottinglog,))

tweepy_int()
tgateway.start()
tdataproc.start()
tplotting.start()
