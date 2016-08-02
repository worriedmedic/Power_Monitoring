import time
import datetime
import requests
import os.path
import csv
import codecs
import urllib2
import json

debug     = True
verbose   = True
internet  = True

## INT: Data that will change every day
today = [None]
yesterday = [None]
tomorrow = [None]
fname = [None]
sheetname =[None]
fdir = [None]

## INT: Helper variables for tides
tide_datetime = [None]
tide_next_time = [None]
tide_next_type = [None]
tide_next_mag = [None]
tide_pre_time = [None]
tide_pre_type = [None]
tide_pre_mag = [None]
tide_list = []
tide_time = [None]
tide_type = [None]
tide_mag = [None]

## INT: Helper variables for sun
sun_list = []
sun_rise = [None]
sun_down = [None]

## INT: Expected Hi and Lo
wunder_site_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ma/cuttyhunk.json'
onlinejson = [None]
forecast = [None]
exp_hi = [None]
exp_lo = [None]

## INT: Cheating the wind data
ch_avg_wind_speed = [None]
ch_wind_dir = [None]
ch_max_wind_speed = [None]

## INT: Data that will change on every packet
buff = [None] * 50
addr  = [None]	
temp  = [None] * 5
press = [None] * 5
humid = [None] * 5
volt  = [None] * 5
rssi  = [None] * 5
wind_speed = [None] * 5
wind_dir = [None] * 5

## INT: Station 0 - Inside the house. Top floor.
temp_0 = [None]

## INT: Station 1 - Inside the house. Bottom floor
temp_1 = [None]

## INT: Station 2 - Outside, near the barn.
tepm_2 = [None]
press_2 = [None]
humid_2 = [None]

## YEARLY SHIT
## Shit to get the tides in a csv. Once its done dont touch it.
## All we gotta do is grab one each new day. Thats it. Simple shieeeeet

if (False):
	tide_text = '8448376_annual.txt'
	tide_csv = 'cutty_tide.csv'
	in_txt = csv.reader(open(tide_text,"rb"), delimiter = '\t')
	temp_csv = csv.writer(open(tide_csv, "wb"))
	temp_csv.writerows(in_txt)
	temp_csv.close()

## SUNRISE - SUNSET SHIT GOES HERE

## Or not, done manually on 2016

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
        
## FUNCTIONS

def get_tide(tide_day):
	## Grab the tide for the day that you input
	## Requires today or tomorrow as input
	with open('cutty_tide.csv', 'rb') as tide_csv:
		tide_reader = csv.reader(tide_csv, delimiter =',')
		day = tide_day.strftime("%Y/%m/%d")
		temp_list = []
		for row in tide_reader:
			if (row[0] == day):
				tide_time = row[2]
				tide_mag = row[3]
				tide_type = row[7]
				temp_list.append([tide_time,tide_type,tide_mag])
	return temp_list

## MAIN LOOP

while(1):
	
	'''
	Executing loop. Code should be running all day.
	Will have daily goals that need to be updated.
	Yearly goals will need to manually done.
	Yearly goals are sunset data, and tide data.
	'''
	## DAILY TASKS
	
	if (today != datetime.date.today()):
		
		'''
		If our value for today is wrong, we have passed onto the next day
		These tasks are:
			Update tide clock for new day
			Update sunrise and sundown
			Update Expected Hi and Lo
			Update Date
			Create new day's log files
		'''
		
		# UPDATE TODAY'S LOGS
		
		try:
			now = time.strftime("%H:%M:%S") # Call time of serial read
			today = datetime.date.today()
			yesterday = datetime.date.today() + datetime.timedelta(days=-1)
			tomorrow = datetime.date.today() + datetime.timedelta(days=1)
			fname = str(today) + '.log'
			fdirectory = 'data_log/' + time.strftime("%Y-%m")
			
		except Exception as e:
			print("TIME UPDATE ERROR", e)

		## GRABBING TIDES
		# WILL PULL TIDE DATA FOR THE FOLLOWING 24 HOURS
		
		if tide_list == []:
			try:
				tide_list = get_tide(today)
				tide_next_time = '12:00 AM'
				tide_datetime = datetime.datetime.strptime(tide_next_time,'%I:%M %p')
				tide_datetime = tide_datetime.replace(today.year,today.month,today.day)
			except Exception as e:
				print("TIDE LIST ERROR", str(today), now, e)
				
		# IMPORT SUNRISE / SUNSET DATA
		
		try:
			with open('Sun_data.csv', 'rb') as sun_csv:
				sun_reader = csv.reader(sun_csv, delimiter =',')
				sun_day = today.strftime("%Y/%m/%d")
				for row in sun_reader:
					if (row[0] == sun_day):
						sun_rise = str(row[1])
						sun_down = str(row[2])
				sun_rise = sun_rise[1]+':'+ sun_rise[2:]
				sun_down = sun_down[0:2] + ':' + sun_down[2:]
		except Exception as e:
			print("SUN TIME ERROR", str(today), now, e)

		## Update expected Hi and Lo
		# Assumptions:
		# 	Internet is working an never quits
		#	API calls to Wunderground work
		#	Wunderground hasnt changed its format on its API

		# Likely will break this out to another if/else that clarifies 
		# if we have internet or not. If we dont have internet, 
		# grab data from yesterday and use that as expected hi and lo

		try:
			if internet:
				if not os.path.isfile(str(today)+'_forecast.json'):
					onlinejson = requests.get(wunder_site_json)
					localjson = open(str(today)+'_forecast.json', 'wb')
					if os.path.isfile(str(yesterday)+'_forecast.json'):
						os.remove(str(yesterday)+'_forecast.json')
					for chunk in onlinejson.iter_content(100000):
						localjson.write(chunk)
					onlinejson.close()
					localjson.close()
					localjson = open(str(today)+'_forecast.json','rb')
					json_string = localjson.read()
					parsed_json = json.loads(json_string)
					exp_hi = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
					exp_lo = parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
					if debug:
						print(exp_hi)
						print(exp_lo)
		except requests.exceptions.RequestException as e:
			print("Wunder JSON Requets Error", str(today), now, e)
		except Exception as e:
			print("Wunder JSON Error", str(today), now, e)

			## GET WIND SPEED AND DIRECTION FROM WUNDERGROUND (CHEATING)

		try:
			ch_avg_wind_speed = parsed_json['forecast']['simpleforecast']['forecastday'][0]['avewind']['mph']
			ch_wind_dir = parsed_json['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir']
			ch_max_wind_speed = parsed_json['forecast']['simpleforecast']['forecastday'][0]['maxwind']['mph']
			if debug:
				print(ch_wind_speed)
				print(ch_wind_dir)
		except Exception as e:
			print("WIND IMPORT ERROR", str(today), time, e)

		### END OF DAILY TASKS, BEGIN STREAMING DATA


	# Update the tide
	# Tide will be output as a list for the day. 
	# In this list will be smaller lists with the values for 
	# Time, High or Low, and magnitude of the tide
	# Should be no more than 5 tides and no fewer than 3.
	# Avg case is 4.
	
	### print (time.strftime('%y:%m:%d:%H:%M:%S')) ### COMMENTED OUT BY LWH 2016/08/01
	
	minute = datetime.datetime.now()

	try:
		while(minute > tide_datetime):
			if len(tide_list)<=1:
				tide_list = get_tide(tomorrow)
				tide_pre_time = tide_next_time
				tide_pre_type = tide_next_type
				tide_pre_mag = tide_next_mag
				tide_next_time = tide_list[0][0]
				tide_next_type = tide_list[0][1]
				tide_next_mag = tide_list[0][2]
				old = tide_datetime
				dummy = datetime.datetime.strptime(tide_next_time,'%I:%M %p')
				tide_datetime = tide_datetime.replace(tomorrow.year, tomorrow.month, tomorrow.day, dummy.hour,dummy.minute)
			else:
				tide_list = tide_list[1:]
				tide_pre_time = tide_next_time
				tide_pre_type = tide_next_type
				tide_pre_mag = tide_next_mag
				tide_next_time = tide_list[0][0]
				tide_next_type = tide_list[0][1]
				tide_next_mag = tide_list[0][2]
				old = tide_datetime
				dummy = datetime.datetime.strptime(tide_next_time,'%I:%M %p')
				tide_datetime = tide_datetime.replace(today.year, today.month, today.day, dummy.hour,dummy.minute)
				if debug:
					print(tide_list)
					print(tide_pre_time)
					print(tide_next_time)
	except Exception as e:
		print("TIDE UPDATE ERROR", str(today), now, e)
	
	now = time.strftime('%H:%M:%S')
	curr_time = time.strftime('%H:%M')
        
    	try:
    		logfile = open('data_log/' + time.strftime("%Y-%m") + '/' + str(today) + '.log',"r")
    		loglines = follow(logfile)
    		for line in loglines:
        		if debug:
        			print line
        except Exception as e:
        	print("LOG FILE OPEN ERROR", str(today), now, e)
        
        try:
                line.split(',')
                addr = line.split(',')[2]
                temp = line.split(',')[3].strip('T')
                press = line.split(',')[4].strip('P')
                humid = line.split(',')[5].strip('H')
                volt = line.split(',')[6].strip('V')
                rssi = line.split(',')[7]
                dew = float(temp) - ((100 - float(humid)) / 5 ) ##FROM DATA PROCESSING PYTHON SCRIPT
                
                if debug:
                	print(addr, temp, press, humid, volt, dew, rssi)
                
                if (int(addr) == 9):
			temp_0 = temp
		elif (int(addr) == 8):
			temp_1 = temp
		elif (int(addr) == 7):
			temp_2 = temp
			press_2 = press
			humid_2 = humid
		
        except Exception as e:
        	print("DATA SPLIT ERROR", str(today), now, e)
        		
        ## Output data to the svg
	
	try:
		output = codecs.open('WX_TEMPLATE.svg', 'r', encoding='utf-8').read()
		output = output.replace('CURDATE', today.strftime("%m/%d/%Y"))
		output = output.replace('CURTIME', str(curr_time))
		output = output.replace('SNRISE', sun_rise)
		output = output.replace('SNSET', sun_down)
		if internet:
			output = output.replace('FORHI', exp_hi)
			output = output.replace('FORLO', exp_lo)
			output = output.replace('WSP', str(ch_avg_wind_speed))
			output = output.replace('WGUS', str(ch_max_wind_speed))
		output = output.replace('TMPE',str(temp_2))
		output = output.replace('TMPI',str(temp_0))
		output = output.replace('TMPG',str(temp))
		output = output.replace('TMPD',str(temp_1))
		output = output.replace('PRESS',  str(press_2))
		output = output.replace('RLHUM',str(humid_2))
		output = output.replace('DWPNT',"{0:.2f}".format(dew))
		output = output.replace('TDNTY',str(tide_pre_type))
		output = output.replace('TDNTM',old.strftime('%H:%M'))
		output = output.replace('TDNLV',str(tide_pre_mag))
		output = output.replace('TDFTY',str(tide_next_type))
		output = output.replace('TDFTM',tide_datetime.strftime('%H:%M'))
		output = output.replace('TDFLV',str(tide_next_mag))
	except Exception as e:
		print("CODECS REPLACE ERROR", str(today), now, e)
	
	try:
		codecs.open('TEST.svg', 'w', encoding='utf-8').write(output)
	except Exception as e:
		print("CODECS WRITE ERROR", str(today), now, e)
