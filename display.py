#/bin/python

import os, sys
import pygame
import time, datetime
import pandas as pd
import numpy as np
import cPickle as pickle
from pygame.locals import *
from standards import *
from icon_def import *

black = (0,0,0)
white = (255,255,255)
uniTmp = unichr(0x2109)

class SmDisplay:
	def __init__(display):
		disp_no = os.getenv('DISPLAY')
		if disp_no:
			print "X Display = {0}".format(disp_no)
		drivers = ['fbcon', 'directfb', 'svgalib']
		found = False
		for driver in drivers:
			if not os.getenv('SDL_VIDEODRIVER'):
				os.putenv('SDL_VIDEODRIVER', driver)
			try:
				pygame.display.init()
			except pygame.error:
				print 'Driver: {0} failed.'.format(driver)
				continue
			found = True
			break
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		print "Framebuffer Size: %d x %d" % (size[0], size[1])
		display.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		display.screen.fill(black)
		pygame.font.init()
		pygame.mouse.set_visible(0)
		pygame.display.update()
		
		display.icon = [ 0, 0, 0, 0 ]
		
		display.xmax = pygame.display.Info().current_w - 10
		display.ymax = pygame.display.Info().current_h - 6
		display.scaleicon = False
		display.iconscale = 1.0
		display.subwinTh = 0.065
		display.txth = 0.115
		display.lrgtxth = 0.4
		display.smtxth = 0.1
		display.smrtxth = 0.065
		display.tinytxth = 0.04
		display.dateYPos = 1
		display.dateYPosSm = 8
	
	def __del___(display):
		'''DESTRUCTOR'''
	
	def daily_wunder_update(display):
		while True:
			now = datetime.datetime.now()
			try:
				display.forecast_data = pd.read_json(wunder_site_forecast_json, typ='series')
				display.astronomy_data = pd.read_json(wunder_site_astronomy_json, typ='series')
			except Exception:
				print("ERROR: DAILY WUNDER UPDATE", now.strftime("%Y-%m-%d %H:%M:%S"))
				traceback.print_exc(file=sys.stdout)
				time.sleep(10)
				continue
			break
	
	def hourly_wunder_update(display):
		while True:
			now = datetime.datetime.now()
			try:
				display.condition_data = pd.read_json(wunder_site_conditions_json, typ='series')
			except Exception:
				print("ERROR: DAILY WUNDER UPDATE", now.strftime("%Y-%m-%d %H:%M:%S"))
				traceback.print_exc(file=sys.stdout)
				time.sleep(10)
				continue
			break
			
	def pickle_update(display):
		display.data0 = pickle.load(open("pickle/data0_pickle.p", "rb"))
		display.data1 = pickle.load(open("pickle/data1_pickle.p", "rb"))
		display.data2 = pickle.load(open("pickle/data2_pickle.p", "rb"))
		display.data3 = pickle.load(open("pickle/data3_pickle.p", "rb"))
		display.data4 = pickle.load(open("pickle/data4_pickle.p", "rb"))
		display.data5 = pickle.load(open("pickle/data5_pickle.p", "rb"))
		display.data6 = pickle.load(open("pickle/data6_pickle.p", "rb"))
		display.data7 = pickle.load(open("pickle/data7_pickle.p", "rb"))
	
	def wx0_disp_update(display):
		display.screen.fill(black)
		xmin = 10
		xmax = display.xmax
		ymax = display.ymax
		fn = "freesans"
		lines = 2
		lc = (255,255,255)
		
		################################################################################
		pygame.draw.line( display.screen, lc, (xmin,0),(xmax,0), lines ) #Top Line
		pygame.draw.line( display.screen, lc, (xmin,0),(xmin,ymax), lines ) #Left Line
		pygame.draw.line( display.screen, lc, (xmin,ymax),(xmax,ymax), lines ) #Bottom Line
		pygame.draw.line( display.screen, lc, (xmax,0),(xmax,ymax), lines ) #Right Line
		pygame.draw.line( display.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines ) #Horizontal Line Under Top
		#pygame.draw.line( display.screen, lc, (xmax*0.5,ymax*0.15),(xmax*0.5,ymax), lines )
		#pygame.draw.line( display.screen, lc, (xmax*0.75,ymax*0.5),(xmax*0.75,ymax), lines )
		
		font = pygame.font.SysFont( fn, int(ymax*(display.txth)), bold=1 )
		lfont = pygame.font.SysFont( fn, int(135), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*(display.smtxth)), bold=1 )
		smfont = pygame.font.SysFont(fn, int(ymax*(display.smrtxth)), bold=1)
		tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
		
		tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
		
		rtm1 = font.render(tm1, True, lc )
		
		display.screen.blit(rtm1, (15,display.dateYPos))
		
		weather_data = {'sunrise'	: '5:42',
				'sunset'	: '19:42'}
		
		sunrise = smfont.render(weather_data['sunrise'], True, lc)
		(srx1, sry1) = sunrise.get_size()
		sunset = smfont.render(weather_data['sunset'], True, lc)
		(ssx1, ssy1) = sunset.get_size()
		
		display.screen.blit(sunrise, (428,2))
		display.screen.blit(sunset, (417,20))
		
		icon_sunrise = pygame.image.load(sd + icons[0]).convert_alpha() #SunRise
		(ix, iy) = icon_sunrise.get_size()
		icon2_sunrise = pygame.transform.scale(icon_sunrise, (int(ix*.12), int(iy*.14)))
		display.screen.blit(icon2_sunrise, (370,4))
		################################################################################
		pygame.draw.line( display.screen, lc, (310,ymax*0.15),(310,ymax*0.6), lines) #Vertical Line @x:310
		pygame.draw.line( display.screen, lc, (xmin,ymax*0.6),(xmax,ymax*0.6), lines)
		
		if display.data0['temperature'][0] < 100:
			temp0 = str(display.data0['temperature'][0])[:4]
		elif display.data0['temperature'][0] >= 100:
			temp0 = str(display.data0['temperature'][0])[:3]
		rtemp0 = lfont.render(temp0, True, lc)
		display.screen.blit(rtemp0, (18, 32))
		
		rsensor0label = font.render(sensor0label, True, lc)
		display.screen.blit(rsensor0label, (317,50))
		
		dfont = pygame.font.SysFont(fn, int(40), bold=1 )
		dtxt = dfont.render(uniTmp, True, lc )
		display.screen.blit(dtxt, (270, 50))
		
		rtemp0time = tinyfont.render(display.data0['time'].strftime("%y-%m-%d %H:%M:%S"), True, lc)
		display.screen.blit(rtemp0time, (15, 165))
		
		rtemp0max = tinyfont.render('Max: ' + str(display.data0['temperature_max'])[:4], True, lc)
		display.screen.blit(rtemp0max, (162, 165))
		
		rtemp0min = tinyfont.render('Min: ' + str(display.data0['temperature_min'])[:4], True, lc)
		display.screen.blit(rtemp0min, (238, 165))
		################################################################################
		tempgraph = pygame.image.load('output/plot_sm_Temperature_sensor_0.png')
		tempgraph2 = pygame.transform.scale(tempgraph, (455, 122))
		display.screen.blit(tempgraph2, (12,192))
		################################################################################
		if display.data0['humidity'][0] == 100:
			humid0 = str(display.data0['humidity'][0])[:3]
		elif display.data0['humidity'][0] < 100:
			humid0 = str(display.data0['humidity'][0])[:4]
		rhumid0 = tinyfont.render(humid0 + '%', True, lc)
		display.screen.blit(rhumid0, (400, 50+50))
		rhumid_label = tinyfont.render('Humid:', True, lc)
		display.screen.blit(rhumid_label, (317, 50+50))
		
		if display.data0['dewpoint'][0] == 100:
			dew0 = str(display.data0['dewpoint'][0])[:3]
		elif display.data0['dewpoint'][0] < 100:
			dew0 = str(display.data0['dewpoint'][0])[:4]
		rdew0 = tinyfont.render(dew0 + " " + uniTmp, True, lc)
		display.screen.blit(rdew0, (400,67+50))
		rdew_label = tinyfont.render('Dewpoint:', True, lc)
		display.screen.blit(rdew_label, (317,67+50))
		
		if display.data0['pressure'][0] >= 1000:
			press0 = str(display.data0['pressure'][0])[:4]
		elif display.data0['dewpoint'][0] < 1000:
			press0 = str(display.data0['pressure'][0])[:5]
		rpress0 = tinyfont.render(press0 + "Hg", True, lc)
		display.screen.blit(rpress0, (400,84+50))
		rpress_label = tinyfont.render('Pressure:', True, lc)
		display.screen.blit(rpress_label, (317,84+50))
		
		volt0 = str(display.data0['voltage'][0])[:4]
		rvolt0 = tinyfont.render(volt0 + "vdc", True, lc)
		display.screen.blit(rvolt0, (400,101+50))
		rvolt_label = tinyfont.render('Voltage:', True, lc)
		display.screen.blit(rvolt_label, (317,101+50))
		
		rssi0 = str(display.data0['rssi'][0])[:2]
		rrssi0 = tinyfont.render(rssi0, True, lc)
		display.screen.blit(rrssi0, (400,118+50))
		rrssi_label = tinyfont.render('RSSI:', True, lc)
		display.screen.blit(rrssi_label, (317,118+50))
		
		pygame.display.update()


d = SmDisplay()
#d.daily_wunder_update()
d.pickle_update()
d.wx0_disp_update()
s = time.localtime().tm_sec
while True:
	if s is not time.localtime().tm_sec:
		s = time.localtime().tm_sec
		d.pickle_update()
		d.wx1_disp_update()
