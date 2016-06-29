# !/bin/python
# Created from https://www.mathworks.com/help/thingspeak/thingtweet-app.html
# Using requests

import os
import time
import datetime
import requests
import os.path

url     = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update'
#delay   = 600 #In Seconds ### REDUNDANT - NOW USING CRONTAB
api_key = 'UERV67G8O01HXYVV' #Key for the ThingSpeak Tweeter API
logging = 'false'
verbose = 'false'

dover_sensor = { #Modified for Dover_Wx_St
    'Inside'        : '123799',
    'Outside'       : '123694',
    'Downstairs'    : '124921',
    'Garage'        : '125305'
    
}

def thingspeaktweet(api_key):
    tweet = "Outside: %%channel_123694_field_2%%F, %%channel_123694_field_4%%%, Inside: %%channel_123799_field_2%%F, %%channel_123799_field_4%%%, Downstairs: %%channel_124921_field_2%%F, %%channel_124921_field_4%%%, Garage: %%channel_125305_field_2%%F, %%channel_125305_field_4%%%, Press: %%channel_123694_field_3%%mb"
    if verbose == 'true':
        print(tweet)
    payload = {'api_key': api_key, 'status': tweet}
    try:
        r = requests.post(url, data=payload)
        time.sleep(1)
        print(now, r.text)
    except requests.exceptions.RequestException as e:
        print(e.text)
        
    if logging == 'true':
        fname = str(today) + '.log'
        fdirectory = 'data_log'
        fmode = 'a' #Append

        if not os.path.exists(fdirectory):
            os.makedirs(fdirectory)
   
        log = now + ',' + r.text + '\n'
        
        outf = open(os.path.join(fdirectory, fname), fmode)
        outf.write(log)
        outf.flush()

try:
    now = time.strftime("%H:%M:%S")
    today = datetime.date.today()
    thingspeaktweet(api_key)
except:
    print("UNKNOWN ERROR")
