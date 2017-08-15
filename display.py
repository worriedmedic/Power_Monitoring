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
		display.data0 = pickle.load(open("data0_pickle.p", "rb"))
		display.data1 = pickle.load(open("data1_pickle.p", "rb"))
		display.data2 = pickle.load(open("data2_pickle.p", "rb"))
		display.data3 = pickle.load(open("data3_pickle.p", "rb"))
		display.data4 = pickle.load(open("data4_pickle.p", "rb"))
		display.data5 = pickle.load(open("data5_pickle.p", "rb"))
		display.data6 = pickle.load(open("data6_pickle.p", "rb"))
		display.data7 = pickle.load(open("data7_pickle.p", "rb"))
	
	def wx1_disp_update(display):
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
		#pygame.draw.line( display.screen, lc, (xmin,ymax*0.5),(xmax,ymax*0.5), lines ) #Horizontal Line at Middle
		#pygame.draw.line( display.screen, lc, (xmax*0.25,ymax*0.5),(xmax*0.25,ymax), lines )
		#pygame.draw.line( display.screen, lc, (xmax*0.5,ymax*0.15),(xmax*0.5,ymax), lines )
		#pygame.draw.line( display.screen, lc, (xmax*0.75,ymax*0.5),(xmax*0.75,ymax), lines )
		
		font = pygame.font.SysFont( fn, int(ymax*(display.txth)), bold=1 )
		lfont = pygame.font.SysFont( fn, int(ymax*(display.lrgtxth)), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*(display.smtxth)), bold=1 )
		smfont = pygame.font.SysFont(fn, int(ymax*(display.smrtxth)), bold=1)
		tinyfont = pygame.font.SysFont(fn, int(ymax*(display.tinytxth)), bold=1)
		
		tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
		
		rtm1 = font.render(tm1, True, lc )
		
		display.screen.blit(rtm1, (15,display.dateYPos))
		
		weather_data = {'sunrise'	: '5:42',
				'sunset'	: '19:42'}
		
		sunrise = smfont.render(weather_data['sunrise'], True, lc)
		(srx1, sry1) = sunrise.get_size()
		sunset = smfont.render(weather_data['sunset'], True, lc)
		(ssx1, ssy1) = sunset.get_size()
		
		display.screen.blit(sunrise, (426,2))
		display.screen.blit(sunset, (415,18))
		
		icon_sunrise = pygame.image.load(sd + icons[0]).convert_alpha() #SunRise
		(ix, iy) = icon_sunrise.get_size()
		icon2_sunrise = pygame.transform.scale(icon_sunrise, (int(ix*.12), int(iy*.14)))
		display.screen.blit(icon2_sunrise, (370,4))
		################################################################################
		if display.data0['temperature'][0] < 100:
			temp0 = str(display.data0['temperature'][0])[:4]
		elif display.data0['temperature'][0] >= 100:
			temp0 = str(display.data0['temperature'][0])[:3]
		dfont = pygame.font.SysFont( fn, int(ymax*(0.5-0.15)*0.5), bold=1 )
		
		rsensor0label = tinyfont.render(sensor0label, True, lc)
		display.screen.blit(rsensor0label, (18,27))
		rtemp0 = lfont.render(temp0, True, lc)
		display.screen.blit(rtemp0, (18, 32))
		
		dtxt = dfont.render(uniTmp, True, lc )
		display.screen.blit(dtxt, (255, 40))
		
		################################################################################
		pygame.display.update()


d = SmDisplay()
d.daily_wunder_update()
d.pickle_update()
d.wx1_disp_update()
s = time.localtime().tm_sec
while True:
	if s is not time.localtime().tm_sec:
		s = time.localtime().tm_sec
		d.pickle_update()
		d.wx1_disp_update()
