import time
import datetime
import requests
import os.path
import csv
import codecs
import urllib2
import json
from lxml import etree
import traceback

debug     = False
verbose   = False
internet  = True

if os.path.isfile('dover.location'):
	location = 'dover'
	template_svg_filename = 'resources/DOVER_WX_TEMPLATE.svg'
	update_freq = 100
	bat1 = '09'
	bat2 = '08'
	bat3 = '07'
	bat4 = '06'
	bat5 = '05'
	if debug:
		print(location)
elif os.path.isfile('cuttyhunk.location'):
	location = 'cuttyhunk'
	template_svg_filename = 'resources/CUTTY_WX_TEMPLATE.svg'
	update_freq = 18
	bat1 = '00'
	bat2 = '01'
	bat3 = '02'
	bat4 = '03'
	bat5 = '04'
	if debug:
		print(location)
else:
	location = 'cuttyhunk' # DEFAULT
	template_svg_filename = 'resources/CUTTY_WX_TEMPLATE.svg'
	update_freq = 18
	bat1 = '00'
	bat2 = '01'
	bat3 = '02'
	bat4 = '03'
	bat5 = '04'
	if debug:
		print(location)

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
if location == 'cuttyhunk':
	wunder_site_forcast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ma/cuttyhunk.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ma/cuttyhunk.json'
elif location == 'dover':
	wunder_site_forcast_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/forecast/q/ny/carmel.json'
	wunder_site_conditions_json = 'http://api.wunderground.com/api/1f86b1c989ac268c/conditions/q/ny/carmel.json'
	
wunder_update_time = [None]
elapsed = [None]
onlinejson = [None]
forecast = [None]
exp_hi = [None]
exp_lo = [None]

## INT: Cheating the wind data
avg_wind_speed = [None]
wind_dir = [None]
max_wind_speed = [None]

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
temp_0 = 0
press_0 = 0
humid_0 = 0
dew_0 = 0

## INT: Station 1 - Inside the house. Bottom floor
temp_1 = 0

## INT: Station 2 - Outside, near the barn.
temp_2 = 0
press_2 = 0
humid_2 = 0

## INT: Station 3
temp_3 = 0

i = 0

## YEARLY SHIT
## Shit to get the tides in a csv. Once its done dont touch it.
## All we gotta do is grab one each new day. Thats it. Simple shieeeeet

if (False):
	tide_text = '8448376_annual.txt'
	tide_csv = 'resources/cutty_tide.csv'
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
	with open('resources/cutty_tide.csv', 'rb') as tide_csv:
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
		now = time.strftime("%H:%M:%S")
		
		# UPDATE TODAY'S LOGS
		
		try:
			now = time.strftime("%H:%M:%S") # Call time of serial read
			today = datetime.date.today()
			yesterday = datetime.date.today() + datetime.timedelta(days=-1)
			tomorrow = datetime.date.today() + datetime.timedelta(days=1)
			fname = str(today) + '.log'
			fdirectory = 'data_log/' + time.strftime("%Y-%m")
			
		except Exception as e:
			print("TIME UPD ERR", str(today), now)
			traceback.print_exc()

		## GRABBING TIDES
		# WILL PULL TIDE DATA FOR THE FOLLOWING 24 HOURS
		
		if tide_list == []:
			try:
				tide_list = get_tide(today)
				tide_next_time = '12:00 AM'
				tide_datetime = datetime.datetime.strptime(tide_next_time,'%I:%M %p')
				tide_datetime = tide_datetime.replace(today.year,today.month,today.day)
			except Exception as e:
				print("TIDE LST ERR", str(today), now)
				traceback.print_exc()
				
		# IMPORT SUNRISE / SUNSET DATA
		
		try:
			with open('resources/Sun_data.csv', 'rb') as sun_csv:
				sun_reader = csv.reader(sun_csv, delimiter =',')
				sun_day = today.strftime("%Y/%m/%d")
				for row in sun_reader:
					if (row[0] == sun_day):
						sun_rise = str(row[1])
						sun_down = str(row[2])
				sun_rise = sun_rise[1]+':'+ sun_rise[2:]
				sun_down = sun_down[0:2] + ':' + sun_down[2:]
		except Exception as e:
			print("SUN TIME ERR", str(today), now)
			traceback.print_exc()

		## Update expected Hi and Lo
		# Assumptions:
		# 	Internet is working an never quits
		#	API calls to Wunderground work
		#	Wunderground hasnt changed its format on its API

		try:
			if internet:
				if not os.path.isfile('resources/' + str(today) + '_forecast.json'):
					try:
						onlinejson = requests.get(wunder_site_forcast_json)
						localjson = open('resources/' + str(today) + '_forecast.json', 'wb')
						if os.path.isfile('resources/' + str(yesterday) + '_forecast.json'):
							os.remove('resources/' + str(yesterday) + '_forecast.json')
						for chunk in onlinejson.iter_content(100000):
							localjson.write(chunk)
						onlinejson.close()
						localjson.close()
					except Exception as e:
						print("WUND FOR JSN LOAD ERR", str(today), now)
						traceback.print_exc()

				localjson = open('resources/' + str(today) + '_forecast.json','rb')
				json_string = localjson.read()
				parsed_json = json.loads(json_string)
				exp_hi = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
				exp_lo = parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
				if debug:
					print(exp_hi, exp_lo)
         	
         	except Exception as e:
			print("WUND FOR JSN READ ERR", str(today), now)
			traceback.print_exc()
	
		# Likely will break this out to another if/else that clarifies 
		# if we have internet or not. If we dont have internet, 
		# grab data from yesterday and use that as expected hi and lo

		### END OF DAILY TASKS, BEGIN STREAMING DATA


	# Update the tide
	# Tide will be output as a list for the day. 
	# In this list will be smaller lists with the values for 
	# Time, High or Low, and magnitude of the tide
	# Should be no more than 5 tides and no fewer than 3.
	# Avg case is 4.
	
	### print (time.strftime('%y:%m:%d:%H:%M:%S')) ### COMMENTED OUT BY LWH 2016/08/01
	
	
	try:
		if internet:
			## Cheat and get wind speed / dir
			if i >= update_freq or i == 0:
				try:
					i = 0
					onlinejson = requests.get(wunder_site_conditions_json)
					localjson = open('resources/' + str(today) + '_conditions.json', 'wb')
					if os.path.isfile('resources/' + str(yesterday) + '_conditions.json'):
						os.remove('resources/' + str(yesterday) + '_conditions.json')
					for chunk in onlinejson.iter_content(100000):
						localjson.write(chunk)
					onlinejson.close()
					localjson.close()
				except Exception as e:
					print("WUND CUR JSN LOAD ERR", str(today), now)
					traceback.print_exc()

				localjson = open('resources/' + str(today) + '_conditions.json','rb')
				json_string = localjson.read()
				parsed_json = json.loads(json_string)
				avg_wind_speed = parsed_json['current_observation']['wind_mph']
				wind_dir = parsed_json['current_observation']['wind_dir']
				max_wind_speed = parsed_json['current_observation']['wind_gust_mph']
				pressure_trend = parsed_json['current_observation']['pressure_trend']
				if debug:
					print(avg_wind_speed, wind_dir, max_wind_speed, pressure_trend)
				
	except Exception as e:
		print("WUND CON JSN READ ERR", str(today), now)
		traceback.print_exc()
	
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
		print("TIDE UPD ERR", str(today), now)
		traceback.print_exc()
	
	now = time.strftime('%H:%M:%S')
	curr_time = time.strftime('%H:%M')
        
	try:
		logfile = open('data_log/' + time.strftime("%Y-%m") + '/' + str(today) + '.log',"r")
		loglines = follow(logfile)
		for line in loglines:
			if debug:
				print line
			i += 1
			now = time.strftime('%H:%M:%S')
			curr_time = time.strftime('%H:%M')

			try:
				line.split(',')
				addr = line.split(',')[2]
				temp = line.split(',')[3].strip('T')
				press = line.split(',')[4].strip('P')
				humid = line.split(',')[5].strip('H')
				volt = line.split(',')[6].strip('V')
				rssi = line.split(',')[7].strip('\n')
				dew = float(temp) - (0.36 * (100 - float(humid))) ##FROM DATA PROCESSING PYTHON SCRIPT

				if debug:
					print(addr, temp, press, humid, volt, dew, rssi)

				if location == 'cuttyhunk':
					if (addr == '01'):
						temp_0 = float(temp) #EXTERIOR
						temp_2 = float(temp)
						press_0 = float(press)
						humid_0 = float(humid)
						dew_0 = float(dew)
					elif (addr == '00'):
						temp_1 = float(temp) #INTERIOR
						temp_3 = float(temp)
				elif location == 'dover':
					if (addr == '09'):
						temp_0 = float(temp) #EXTERIOR
						press_0 = float(press)
						humid_0 = float(humid)
						dew_0 = float(dew)
					elif (addr == '08'):
						temp_1 = float(temp) #INTERIOR
					elif (addr == '05'): 
						temp_2 = float(temp) #ATTIC
					elif (addr == '07'):
						temp_3 = float(temp)

			except Exception as e:
				print("DATA SPLIT ERR", str(today), now)
				traceback.print_exc()
        		
			## UPDATE BATTERY LEVEL ON SVG
			try:
				tree = etree.parse(open(template_svg_filename, 'r'))
        			
				if (addr == bat1):
					if (0 <= float(volt) < 80):
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b00Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat1, " - 0 to 80")
					elif (80 <= float(volt) < 85): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b00Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat1":
									element.attrib['class'] = ''
								if element.get("id") == "b00Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat1, " - 80 to 85")
					elif (85 <= float(volt) < 90): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b00Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat2":
									element.attrib['class'] = ''
								if element.get("id") == "b00Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat1, " - 80 to 90")
					elif (90 <= float(volt) < 95): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b00Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat3":
									element.attrib['class'] = ''
								if element.get("id") == "b00Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat1, " - 90 to 95")
					elif (95 <= float(volt) < 100): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b00Bat4":
									element.attrib['class'] = ''
								if element.get("id") == "b00Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b00Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat1, " - 95 to 100")
				elif (addr == bat2):
					if (0 <= float(volt) < 80):
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b01Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat2, " - 0 to 80")
					elif (80 <= float(volt) < 85): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b01Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat1":
									element.attrib['class'] = ''
								if element.get("id") == "b01Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat2 + " - 80 to 50")
					elif (80 <= float(volt) < 90): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b01Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat2":
									element.attrib['class'] = ''
								if element.get("id") == "b01Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat2, " - 80 to 90")
					elif (90 <= float(volt) < 95): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b01Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat3":
									element.attrib['class'] = ''
								if element.get("id") == "b01Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat2, " - 90 to 95")
					elif (95 <= float(volt) < 100): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b01Bat4":
									element.attrib['class'] = ''
								if element.get("id") == "b01Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b01Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat2, " - 95 to 100")
				elif (addr == bat3):
					if (0 <= float(volt) < 80):
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b02Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat3, " - 0 to 80")
					elif (80 <= float(volt) < 85): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b02Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat1":
									element.attrib['class'] = ''
								if element.get("id") == "b02Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat3, " - 80 to 85")
					elif (85 <= float(volt) < 90): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b02Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat2":
									element.attrib['class'] = ''
								if element.get("id") == "b02Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat3, " - 85 to 90")
					elif (90 <= float(volt) < 95): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b02Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat3":
									element.attrib['class'] = ''
								if element.get("id") == "b02Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat3, " - 90 to 95")
					elif (95 <= float(volt) < 100): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b02Bat4":
									element.attrib['class'] = ''
								if element.get("id") == "b02Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b02Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat3, " - 95 to 100")
				elif (addr == bat4):
					if (0 <= float(volt) < 80):
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b03Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat4, " - 0 to 80")
					elif (80 <= float(volt) < 85): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b03Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat1":
									element.attrib['class'] = ''
								if element.get("id") == "b03Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat4, " - 80 to 85")
					elif (85 <= float(volt) < 90): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b03Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat2":
									element.attrib['class'] = ''
								if element.get("id") == "b03Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat4, " - 85 to 90")
					elif (90 <= float(volt) < 95): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b03Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat3":
									element.attrib['class'] = ''
								if element.get("id") == "b03Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat4, " - 90 to 95")
					elif (95 <= float(volt) < 100): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b03Bat4":
									element.attrib['class'] = ''
								if element.get("id") == "b03Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b03Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat4, " - 95 to 100")
				elif (addr == bat5):
					if (0 <= float(volt) < 80):
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b04Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat5, " - 0 to 80")
					elif (80 <= float(volt) < 85): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b04Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat1":
									element.attrib['class'] = ''
								if element.get("id") == "b04Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat5, " - 80 to 85")
					elif (85 <= float(volt) < 90): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b04Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat2":
									element.attrib['class'] = ''
								if element.get("id") == "b04Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat5, " - 80 to 90")
					elif (90 <= float(volt) < 95): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b04Bat4":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat3":
									element.attrib['class'] = ''
								if element.get("id") == "b04Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat5, " - 90 to 95")
					elif (95 <= float(volt) < 100): 
						for element in tree.iter():
							if element.tag.split("}")[1] == "path":
								if element.get("id") == "b04Bat4":
									element.attrib['class'] = ''
								if element.get("id") == "b04Bat3":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat2":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat1":
									element.attrib['class'] = 'st3'
								if element.get("id") == "b04Bat0":
									element.attrib['class'] = ''
								if debug:
									print(bat5, " - 95 to 100")
									
				tree.write(template_svg_filename)
			
			except Exception as e:
				print("BAT SVG UPD ERR", str(today), now)
				traceback.print_exc()
			
			try:
				tree = etree.parse(open(template_svg_filename, 'r'))
				
				if pressure_trend in ['+']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "ple":
								element.attrib['class'] = 'st3'
							if element.get("id") == "pup":
								element.attrib['class'] = ''
							if element.get("id") == "pdn":
								element.attrib['class'] = 'st3'
				elif pressure_trend in ['0']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "ple":
								element.attrib['class'] = ''
							if element.get("id") == "pup":
								element.attrib['class'] = 'st3'
							if element.get("id") == "pdn":
								element.attrib['class'] = 'st3'
				elif pressure_trend in ['-']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "ple":
								element.attrib['class'] = 'st3'
							if element.get("id") == "pup":
								element.attrib['class'] = 'st3'
							if element.get("id") == "pdn":
								element.attrib['class'] = ''
	
				tree.write('output/weather-script-output.svg')
			except Exception as e:
				print("PRES TND SVG UPD ERR", str(today), now, e, traceback.extract_stack())
					
			try:
				tree = etree.parse(open('output/weather-script-output.svg', 'r'))
				
				if wind_dir in ['NNW', 'N', 'NNE', 'North']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = ''
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "NORTH")
				elif wind_dir in ['NE']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = ''
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "NORTH EAST")
				elif wind_dir in ['ENE', 'E', 'ESE', 'East']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = ''
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "EAST")
				elif wind_dir in ['SE']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = ''
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "SOUTH EAST")
				elif wind_dir in ['SSE', 'S', 'SSW', 'South']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = ''
							elif element.get("id") == "wdsw":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "SOUTH")
				elif wind_dir in ['SW']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = ''
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "SOUTH WEST")
				elif wind_dir in ['WSW', 'W', 'WNW', 'West']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = ''
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = 'st3'
							if debug:
								print(wind_dir, "WEST")
				elif wind_dir in ['NW']:
					for element in tree.iter():
						if element.tag.split("}")[1] == "path":
							if element.get("id") == "wdno":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdne":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdea":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdse":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdso":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdsw":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdwe":
								element.attrib['class'] = 'st3'
							elif element.get("id") == "wdnw":
								element.attrib['class'] = ''
							if debug:
								print(wind_dir, "NORTH WEST")

				tree.write('output/weather-script-output.svg')
			except Exception as e:
			 	print("WIND SVG UPD ERR", str(today), now)
			 	traceback.print_exc()
	
			## Output data to the svg
        		
			try:
				output = codecs.open('output/weather-script-output.svg', 'r', encoding='utf-8').read()
				output = output.replace('CURDATE', today.strftime("%m/%d/%Y"))
				output = output.replace('CURTIME', str(curr_time))
				output = output.replace('SNRISE', sun_rise)
				output = output.replace('SNSET', sun_down)
				if internet:
					output = output.replace('FORHI', str(exp_hi))
					output = output.replace('FORLO', str(exp_lo))
					output = output.replace('WSP', str(avg_wind_speed))
					output = output.replace('WGUS', str(max_wind_speed))

				if temp_0 >= 100:
					output = output.replace('TMPE', "{0:.1f}".format(temp_0))
				elif temp_0 < 100:
					output = output.replace('TMPE', "{0:.2f}".format(temp_0))

				if temp_1 >= 100:
					output = output.replace('TMPI', "{0:.1f}".format(temp_1))
				elif temp_1 < 100:
					output = output.replace('TMPI', "{0:.2f}".format(temp_1))

				if temp_2 >= 100:
					output = output.replace('TMPG', "{0:.1f}".format(temp_2))
				elif temp_2 < 100:
					output = output.replace('TMPG', "{0:.2f}".format(temp_2))

				if temp_3 >= 100:
					output = output.replace('TMPD', "{0:.1f}".format(temp_3))
				elif temp_3 < 100:
					output = output.replace('TMPD', "{0:.2f}".format(temp_3))

				if press_0 >= 1000:
					output = output.replace('PRESS', "{0:.0f}".format(press_0))
				elif press_0 < 1000:
					output = output.replace('PRESS', "{0:.1f}".format(press_0))

				output = output.replace('RLHUM', "{0:.2f}".format(humid_0))
				output = output.replace('DWPNT', "{0:.2f}".format(dew_0))
				output = output.replace('TDNTY', str(tide_pre_type))
				output = output.replace('TDNTM', old.strftime('%H:%M'))
				output = output.replace('TDNLV', str(tide_pre_mag))
				output = output.replace('TDFTY', str(tide_next_type))
				output = output.replace('TDFTM', tide_datetime.strftime('%H:%M'))
				output = output.replace('TDFLV', str(tide_next_mag))
			except Exception as e:
				print("CODEC REPLACE ERR", str(today), now, e, traceback.extract_stack())
	
			try:
				codecs.open('output/weather-script-output.svg', 'w', encoding='utf-8').write(output)
			except Exception as e:
				print("SVG WRITE ERR", str(today), now, e, traceback.extract_stack())
			
			break
	
	except IOError as e:
		print("LOG FILE IO ERR", str(today), now)
		traceback.print_exc()
		time.sleep(20)

	except Exception as e:
        	print("GENERIC LOG FILE ERR", str(today), now)
        	traceback.print_exc()
