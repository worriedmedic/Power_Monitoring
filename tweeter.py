# !/bin/python
# Created from https://www.mathworks.com/help/thingspeak/thingtweet-app.html
# Using requests
# # FOR USE WITH DOVER WX ST DATA (API KEY IS SPECIFIC)

import os
import time
import datetime
import requests
import os.path
import traceback

url     = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update'
logging = False
debug   = False

if os.path.isfile('dover.location'):
    api_key = 'UERV67G8O01HXYVV' #Key for the ThingSpeak Tweeter API
    tweet = "Outside: %%channel_123694_field_2%%F, %%channel_123694_field_4%%%, Inside: %%channel_123799_field_2%%F, %%channel_123799_field_4%%%, Downstairs: %%channel_124921_field_2%%F, %%channel_124921_field_4%%%, Garage: %%channel_125305_field_2%%F, %%channel_125305_field_4%%%, Attic: %%channel_130195_field_2%%F, %%channel_130195_field_4%%%, Press: %%channel_123694_field_3%%mb"
elif os.path.isfile('cuttyhunk.location'):
    api_key = 'EC7AV1MRRERF7GAG' #Key for the ThingSpeak Tweeter API
    tweet = "Outside: %%channel_116278_field_2%%F, %%channel_116278_field_4%%%, Inside: %%channel_116348_field_2%%F, %%channel_116348_field_4%%%, Press: %%channel_116278_field_3%%mb"

def thingspeaktweet(api_key):
    if debug:
        print(tweet)
    payload = {'api_key': api_key, 'status': tweet}
    try:
        r = requests.post(url, data=payload)
        #time.sleep(1)
        if debug:
            print(str(today), now, r.text)
            
    except requests.exceptions.RequestException as e:
        print("TWEETAPI REQUESTS ERROR", str(today), now, e, traceback.extract_stack())
    except Exception as e:
        print("TWEETAPI GENERIC ERROR", str(today), now, e, traceback.extract_stack())
        
    if logging:
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
            print("DATA LOG ERROR", today, now, e, traceback.extract_stack())

try:
    now = time.strftime("%H:%M:%S")
    today = str(datetime.date.today())
    thingspeaktweet(api_key)
except Exception as e:
    print("GENERIC ERROR", today, now, e, traceback.extract_stack())
