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
api_key = 'EC7AV1MRRERF7GAG' #Key for the ThingSpeak Tweeter API
logging = 'false'
verbose = 'false'

dover_sensor = { #Modified for Dover_Wx_St
    'Inside'        : '123799',
    'Outside'       : '123694',
    'Downstairs'    : '124921',
    'Garage'        : '125305',
    'Attic'         : '130195'
    
}

cutty_sensor = {
    'Outside'       : '116278'
    'Inside'        : '116348'
}

def thingspeaktweet(api_key):
    tweet = "Outside: %%channel_116278_field_2%%F, %%channel_116278_field_4%%%, Inside: %%channel_116348_field_2%%F, %%channel_116348_field_4%%%, Press: %%channel_116278_field_3%%mb"
    if verbose == 'true':
        print(tweet)
    payload = {'api_key': api_key, 'status': tweet}
    try:
        r = requests.post(url, data=payload)
        time.sleep(1)
        if verbose == 'true':
            print(str(today), str(now), r.text)
            
    except requests.exceptions.RequestException as e:
        print("TWEETAPI REQUESTS ERROR", today, now, e)
    except Exception as e:
        print("TWEETAPI GENERIC ERROR", today, now, e)
        
    if logging == 'true':
        try:
            fname = str(today) + '.log'
            fdirectory = 'data_log'
            fmode = 'a' #Append

            if not os.path.exists(fdirectory):
                os.makedirs(fdirectory)
   
            log = today + ',' + now + ',' + r + '\n'
        
            outf = open(os.path.join(fdirectory, fname), fmode)
            outf.write(log)
            outf.flush()
        except Exception as e:
            print("DATA LOG ERROR", today, now, e)

try:
    now = time.strftime("%H:%M:%S")
    today = str(datetime.date.today())
    thingspeaktweet(api_key)
except Exception as e:
    print("GENERIC ERROR", today, now, e)
