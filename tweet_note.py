import time
from twitter_creds import *
import tweepy
import threading

gatewaylog = '/home/pi/Power_Monitoring/data_log/Gateway_Logger.log'
dataprocesslog = '/home/pi/Power_Monitoring/data_log/Data_to_SVG.log'
plottinglog = '/home/pi/Power_Monitoring/data_log/Matplotlib-plot.log'
displaylog = '/home/pi/Power_Monitoring/data_log/display.log'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
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


def logfollower(filepath,loc):
	try:
		logfile = open(filepath)
		loglines = follow(logfile)
		for line in loglines:
			print line
			try:
				if line.startswith("('ERROR") or line.startswith('serial') or line.startswith('pygame.error'):
					api.update_status(loc + line[:130])
			except tweepy.TweepError as e:
				print(e.reason)
	except Exception:
		print("ERROR: LOGFOLLOWER DEF", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		traceback.print_exc(file=sys.stdout)

tgateway = threading.Thread(target=logfollower, args=(gatewaylog,'GATE:',))
tdataproc = threading.Thread(target=logfollower, args=(dataprocesslog,'DATA:',))
tplotting = threading.Thread(target=logfollower, args=(plottinglog,'PLOT:'))
tdisplay = threading.Thread(target=logfollower, args=(displaylog,'DISP:'))

tgateway.daemon = True
tdataproc.daemon = True
tplotting.daemon = True
tdisplay.daemon = True

tgateway.start()
tdataproc.start()
tplotting.start()
tdisplay.start()

running = True
while running:
	try:
		pass
	except KeyboardInterrupt:
		running = False
