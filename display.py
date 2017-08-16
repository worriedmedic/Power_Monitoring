#/bin/python

import os, sys
import pygame
import time, datetime
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
	
	def pickle_update(display):
		display.data0 = pickle.load(open("pickle/data0_pickle.p", "rb"))
		display.data1 = pickle.load(open("pickle/data1_pickle.p", "rb"))
		display.data2 = pickle.load(open("pickle/data2_pickle.p", "rb"))
		display.data3 = pickle.load(open("pickle/data3_pickle.p", "rb"))
		display.data4 = pickle.load(open("pickle/data4_pickle.p", "rb"))
		display.data5 = pickle.load(open("pickle/data5_pickle.p", "rb"))
		display.data6 = pickle.load(open("pickle/data6_pickle.p", "rb"))
		display.data7 = pickle.load(open("pickle/data7_pickle.p", "rb"))
		display.weather = pickle.load(open("pickle/weather_pickle.p", "rb"))
		display.tides = pickle.load(open("pickle/tide_pickle.p", "rb"))
	
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
		
		font = pygame.font.SysFont( fn, int(ymax*(display.txth)), bold=1 )
		lfont = pygame.font.SysFont( fn, int(135), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*(display.smtxth)), bold=1 )
		smfont = pygame.font.SysFont(fn, int(ymax*(display.smrtxth)), bold=1)
		tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
		
		tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
		
		rtm1 = font.render(tm1, True, lc )
		
		display.screen.blit(rtm1, (15,display.dateYPos))
		
		weather_data = {'sunrise'	: display.weather['sunrise'],
				'sunset'	: display.weather['sunset']}
		
		sunrise = smfont.render(weather_data['sunrise'], True, lc)
		(srx1, sry1) = sunrise.get_size()
		sunset = smfont.render(weather_data['sunset'], True, lc)
		(ssx1, ssy1) = sunset.get_size()
		
		display.screen.blit(sunrise, (428,2))
		display.screen.blit(sunset, (417,20))
		################################################################################
		pygame.draw.line( display.screen, lc, (310,ymax*0.15),(310,ymax*0.6), lines) #Vertical Line @x:310
		pygame.draw.line( display.screen, lc, (xmin,ymax*0.6),(xmax,ymax*0.6), lines)
		
		if display.data0['temperature'][0] < 100:
			temp = str(display.data0['temperature'][0])[:4]
		elif display.data0['temperature'][0] >= 100:
			temp = str(display.data0['temperature'][0])[:3]
		rtemp = lfont.render(temp, True, lc)
		display.screen.blit(rtemp, (18, 32))
		
		rsensorlabel = font.render(sensor0label[:7], True, lc)
		display.screen.blit(rsensorlabel, (317,50))
		
		dfont = pygame.font.SysFont(fn, int(40), bold=1 )
		dtxt = dfont.render(uniTmp, True, lc )
		display.screen.blit(dtxt, (270, 50))
		
		rtemptime = tinyfont.render(display.data0['time'].strftime("%y-%m-%d %H:%M:%S"), True, lc)
		display.screen.blit(rtemptime, (15, 165))
		
		rtempmax = tinyfont.render('Max: ' + str(display.data0['temperature_max'])[:4], True, lc)
		display.screen.blit(rtempmax, (162, 165))
		
		rtempmin = tinyfont.render('Min: ' + str(display.data0['temperature_min'])[:4], True, lc)
		display.screen.blit(rtempmin, (238, 165))
		################################################################################
		tempgraph = pygame.image.load('output/plot_sm_Temperature_sensor_0.png')
		tempgraph2 = pygame.transform.scale(tempgraph, (455, 122))
		display.screen.blit(tempgraph2, (12,192))
		################################################################################
		if display.data0['humidity'][0] == 100:
			humid = str(display.data0['humidity'][0])[:3]
		elif display.data0['humidity'][0] < 100:
			humid = str(display.data0['humidity'][0])[:4]
		rhumid = tinyfont.render(humid + '%', True, lc)
		display.screen.blit(rhumid, (400, 50+50))
		rhumid_label = tinyfont.render('Humid:', True, lc)
		display.screen.blit(rhumid_label, (317, 50+50))
		
		if display.data0['dewpoint'][0] == 100:
			dew = str(display.data0['dewpoint'][0])[:3]
		elif display.data0['dewpoint'][0] < 100:
			dew = str(display.data0['dewpoint'][0])[:4]
		rdew = tinyfont.render(dew + " " + uniTmp, True, lc)
		display.screen.blit(rdew, (400,67+50))
		rdew_label = tinyfont.render('Dewpoint:', True, lc)
		display.screen.blit(rdew_label, (317,67+50))
		
		if display.data0['pressure'][0] >= 1000:
			press = str(display.data0['pressure'][0])[:4]
		elif display.data0['dewpoint'][0] < 1000:
			press = str(display.data0['pressure'][0])[:5]
		rpress = tinyfont.render(press + "Hg", True, lc)
		display.screen.blit(rpress, (400,84+50))
		rpress_label = tinyfont.render('Pressure:', True, lc)
		display.screen.blit(rpress_label, (317,84+50))
		
		volt = str(display.data0['voltage'][0])[:4]
		rvolt = tinyfont.render(volt + "vdc", True, lc)
		display.screen.blit(rvolt, (400,101+50))
		rvolt_label = tinyfont.render('Voltage:', True, lc)
		display.screen.blit(rvolt_label, (317,101+50))
		
		rssi = str(display.data0['rssi'][0])[:2]
		rrssi = tinyfont.render(rssi, True, lc)
		display.screen.blit(rrssi, (400,118+50))
		rrssi_label = tinyfont.render('RSSI:', True, lc)
		display.screen.blit(rrssi_label, (317,118+50))
		
		pygame.display.update()
		
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
		
		font = pygame.font.SysFont( fn, int(ymax*(display.txth)), bold=1 )
		lfont = pygame.font.SysFont( fn, int(135), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*(display.smtxth)), bold=1 )
		smfont = pygame.font.SysFont(fn, int(ymax*(display.smrtxth)), bold=1)
		tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
		
		tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
		
		rtm1 = font.render(tm1, True, lc )
		
		display.screen.blit(rtm1, (15,display.dateYPos))
		
		weather_data = {'sunrise'	: display.weather['sunrise'],
				'sunset'	: display.weather['sunset']}
		
		sunrise = smfont.render(weather_data['sunrise'], True, lc)
		(srx1, sry1) = sunrise.get_size()
		sunset = smfont.render(weather_data['sunset'], True, lc)
		(ssx1, ssy1) = sunset.get_size()
		
		display.screen.blit(sunrise, (428,2))
		display.screen.blit(sunset, (417,20))
		################################################################################
		pygame.draw.line( display.screen, lc, (310,ymax*0.15),(310,ymax*0.6), lines) #Vertical Line @x:310
		pygame.draw.line( display.screen, lc, (xmin,ymax*0.6),(xmax,ymax*0.6), lines)
		
		if display.data1['temperature'][0] < 100:
			temp = str(display.data1['temperature'][0])[:4]
		elif display.data1['temperature'][0] >= 100:
			temp = str(display.data1['temperature'][0])[:3]
		rtemp = lfont.render(temp, True, lc)
		display.screen.blit(rtemp, (18, 32))
		
		rsensorlabel = font.render(sensor1label[:7], True, lc)
		display.screen.blit(rsensorlabel, (317,50))
		
		dfont = pygame.font.SysFont(fn, int(40), bold=1 )
		dtxt = dfont.render(uniTmp, True, lc )
		display.screen.blit(dtxt, (270, 50))
		
		rtemptime = tinyfont.render(display.data1['time'].strftime("%y-%m-%d %H:%M:%S"), True, lc)
		display.screen.blit(rtemptime, (15, 165))
		
		rtempmax = tinyfont.render('Max: ' + str(display.data1['temperature_max'])[:4], True, lc)
		display.screen.blit(rtempmax, (162, 165))
		
		rtempmin = tinyfont.render('Min: ' + str(display.data1['temperature_min'])[:4], True, lc)
		display.screen.blit(rtempmin, (238, 165))
		################################################################################
		tempgraph = pygame.image.load('output/plot_sm_Temperature_sensor_1.png')
		tempgraph2 = pygame.transform.scale(tempgraph, (455, 122))
		display.screen.blit(tempgraph2, (12,192))
		################################################################################
		if display.data1['humidity'][0] == 100:
			humid = str(display.data1['humidity'][0])[:3]
		elif display.data1['humidity'][0] < 100:
			humid = str(display.data1['humidity'][0])[:4]
		rhumid = tinyfont.render(humid + '%', True, lc)
		display.screen.blit(rhumid, (400, 50+50))
		rhumid_label = tinyfont.render('Humid:', True, lc)
		display.screen.blit(rhumid_label, (317, 50+50))
		
		if display.data1['dewpoint'][0] == 100:
			dew = str(display.data1['dewpoint'][0])[:3]
		elif display.data1['dewpoint'][0] < 100:
			dew = str(display.data1['dewpoint'][0])[:4]
		rdew = tinyfont.render(dew + " " + uniTmp, True, lc)
		display.screen.blit(rdew, (400,67+50))
		rdew_label = tinyfont.render('Dewpoint:', True, lc)
		display.screen.blit(rdew_label, (317,67+50))
		
		if display.data1['pressure'][0] >= 1000:
			press = str(display.data1['pressure'][0])[:4]
		elif display.data1['dewpoint'][0] < 1000:
			press = str(display.data1['pressure'][0])[:5]
		rpress = tinyfont.render(press + "Hg", True, lc)
		display.screen.blit(rpress, (400,84+50))
		rpress_label = tinyfont.render('Pressure:', True, lc)
		display.screen.blit(rpress_label, (317,84+50))
		
		volt = str(display.data1['voltage'][0])[:4]
		rvolt = tinyfont.render(volt + "vdc", True, lc)
		display.screen.blit(rvolt, (400,101+50))
		rvolt_label = tinyfont.render('Voltage:', True, lc)
		display.screen.blit(rvolt_label, (317,101+50))
		
		rssi = str(display.data1['rssi'][0])[:2]
		rrssi = tinyfont.render(rssi, True, lc)
		display.screen.blit(rrssi, (400,118+50))
		rrssi_label = tinyfont.render('RSSI:', True, lc)
		display.screen.blit(rrssi_label, (317,118+50))
		
		pygame.display.update()
		
	def wx2_disp_update(display):
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
		
		font = pygame.font.SysFont( fn, int(ymax*(display.txth)), bold=1 )
		lfont = pygame.font.SysFont( fn, int(135), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*(display.smtxth)), bold=1 )
		smfont = pygame.font.SysFont(fn, int(ymax*(display.smrtxth)), bold=1)
		tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
		
		tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
		
		rtm1 = font.render(tm1, True, lc )
		
		display.screen.blit(rtm1, (15,display.dateYPos))
		
		weather_data = {'sunrise'	: display.weather['sunrise'],
				'sunset'	: display.weather['sunset']}
		
		sunrise = smfont.render(weather_data['sunrise'], True, lc)
		(srx1, sry1) = sunrise.get_size()
		sunset = smfont.render(weather_data['sunset'], True, lc)
		(ssx1, ssy1) = sunset.get_size()
		
		display.screen.blit(sunrise, (428,2))
		display.screen.blit(sunset, (417,20))
		################################################################################
		pygame.draw.line( display.screen, lc, (310,ymax*0.15),(310,ymax*0.6), lines) #Vertical Line @x:310
		pygame.draw.line( display.screen, lc, (xmin,ymax*0.6),(xmax,ymax*0.6), lines)
		
		if display.data2['temperature'][0] < 100:
			temp = str(display.data2['temperature'][0])[:4]
		elif display.data2['temperature'][0] >= 100:
			temp = str(display.data2['temperature'][0])[:3]
		rtemp = lfont.render(temp, True, lc)
		display.screen.blit(rtemp, (18, 32))
		
		rsensorlabel = font.render(sensor2label[:7], True, lc)
		display.screen.blit(rsensorlabel, (317,50))
		
		dfont = pygame.font.SysFont(fn, int(40), bold=1 )
		dtxt = dfont.render(uniTmp, True, lc )
		display.screen.blit(dtxt, (270, 50))
		
		rtemptime = tinyfont.render(display.data2['time'].strftime("%y-%m-%d %H:%M:%S"), True, lc)
		display.screen.blit(rtemptime, (15, 165))
		
		rtempmax = tinyfont.render('Max: ' + str(display.data2['temperature_max'])[:4], True, lc)
		display.screen.blit(rtempmax, (162, 165))
		
		rtempmin = tinyfont.render('Min: ' + str(display.data2['temperature_min'])[:4], True, lc)
		display.screen.blit(rtempmin, (238, 165))
		################################################################################
		tempgraph = pygame.image.load('output/plot_sm_Temperature_sensor_2.png')
		tempgraph2 = pygame.transform.scale(tempgraph, (455, 122))
		display.screen.blit(tempgraph2, (12,192))
		################################################################################
		if display.data2['humidity'][0] == 100:
			humid = str(display.data2['humidity'][0])[:3]
		elif display.data2['humidity'][0] < 100:
			humid = str(display.data2['humidity'][0])[:4]
		rhumid = tinyfont.render(humid + '%', True, lc)
		display.screen.blit(rhumid, (400, 50+50))
		rhumid_label = tinyfont.render('Humid:', True, lc)
		display.screen.blit(rhumid_label, (317, 50+50))
		
		if display.data2['dewpoint'][0] == 100:
			dew = str(display.data2['dewpoint'][0])[:3]
		elif display.data2['dewpoint'][0] < 100:
			dew = str(display.data2['dewpoint'][0])[:4]
		rdew = tinyfont.render(dew + " " + uniTmp, True, lc)
		display.screen.blit(rdew, (400,67+50))
		rdew_label = tinyfont.render('Dewpoint:', True, lc)
		display.screen.blit(rdew_label, (317,67+50))
		
		if display.data2['pressure'][0] >= 1000:
			press = str(display.data2['pressure'][0])[:4]
		elif display.data2['dewpoint'][0] < 1000:
			press = str(display.data2['pressure'][0])[:5]
		rpress = tinyfont.render(press + "Hg", True, lc)
		display.screen.blit(rpress, (400,84+50))
		rpress_label = tinyfont.render('Pressure:', True, lc)
		display.screen.blit(rpress_label, (317,84+50))
		
		volt = str(display.data2['voltage'][0])[:4]
		rvolt = tinyfont.render(volt + "vdc", True, lc)
		display.screen.blit(rvolt, (400,101+50))
		rvolt_label = tinyfont.render('Voltage:', True, lc)
		display.screen.blit(rvolt_label, (317,101+50))
		
		rssi = str(display.data2['rssi'][0])[:2]
		rrssi = tinyfont.render(rssi, True, lc)
		display.screen.blit(rrssi, (400,118+50))
		rrssi_label = tinyfont.render('RSSI:', True, lc)
		display.screen.blit(rrssi_label, (317,118+50))
		
		pygame.display.update()
	
	def wx3_disp_update(display):
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
		
		font = pygame.font.SysFont( fn, int(ymax*(display.txth)), bold=1 )
		lfont = pygame.font.SysFont( fn, int(135), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*(display.smtxth)), bold=1 )
		smfont = pygame.font.SysFont(fn, int(ymax*(display.smrtxth)), bold=1)
		tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
		
		tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
		
		rtm1 = font.render(tm1, True, lc )
		
		display.screen.blit(rtm1, (15,display.dateYPos))
		
		weather_data = {'sunrise'	: display.weather['sunrise'],
				'sunset'	: display.weather['sunset']}
		
		sunrise = smfont.render(weather_data['sunrise'], True, lc)
		(srx1, sry1) = sunrise.get_size()
		sunset = smfont.render(weather_data['sunset'], True, lc)
		(ssx1, ssy1) = sunset.get_size()
		
		display.screen.blit(sunrise, (428,2))
		display.screen.blit(sunset, (417,20))
		################################################################################
		pygame.draw.line( display.screen, lc, (310,ymax*0.15),(310,ymax*0.6), lines) #Vertical Line @x:310
		pygame.draw.line( display.screen, lc, (xmin,ymax*0.6),(xmax,ymax*0.6), lines)
		
		if display.data3['temperature'][0] < 100:
			temp = str(display.data2['temperature'][0])[:4]
		elif display.data3['temperature'][0] >= 100:
			temp = str(display.data2['temperature'][0])[:3]
		rtemp = lfont.render(temp, True, lc)
		display.screen.blit(rtemp, (18, 32))
		
		rsensorlabel = font.render(sensor2label[:7], True, lc)
		display.screen.blit(rsensorlabel, (317,50))
		
		dfont = pygame.font.SysFont(fn, int(40), bold=1 )
		dtxt = dfont.render(uniTmp, True, lc )
		display.screen.blit(dtxt, (270, 50))
		
		rtemptime = tinyfont.render(display.data3['time'].strftime("%y-%m-%d %H:%M:%S"), True, lc)
		display.screen.blit(rtemptime, (15, 165))
		
		rtempmax = tinyfont.render('Max: ' + str(display.data3['temperature_max'])[:4], True, lc)
		display.screen.blit(rtempmax, (162, 165))
		
		rtempmin = tinyfont.render('Min: ' + str(display.data3['temperature_min'])[:4], True, lc)
		display.screen.blit(rtempmin, (238, 165))
		################################################################################
		tempgraph = pygame.image.load('output/plot_sm_Temperature_sensor_3.png')
		tempgraph2 = pygame.transform.scale(tempgraph, (455, 122))
		display.screen.blit(tempgraph2, (12,192))
		################################################################################
		if display.data3['humidity'][0] == 100:
			humid = str(display.data3['humidity'][0])[:3]
		elif display.data2['humidity'][0] < 100:
			humid = str(display.data3['humidity'][0])[:4]
		rhumid = tinyfont.render(humid + '%', True, lc)
		display.screen.blit(rhumid, (400, 50+50))
		rhumid_label = tinyfont.render('Humid:', True, lc)
		display.screen.blit(rhumid_label, (317, 50+50))
		
		if display.data3['dewpoint'][0] == 100:
			dew = str(display.data3['dewpoint'][0])[:3]
		elif display.data2['dewpoint'][0] < 100:
			dew = str(display.data3['dewpoint'][0])[:4]
		rdew = tinyfont.render(dew + " " + uniTmp, True, lc)
		display.screen.blit(rdew, (400,67+50))
		rdew_label = tinyfont.render('Dewpoint:', True, lc)
		display.screen.blit(rdew_label, (317,67+50))
		
		if display.data2['pressure'][0] >= 1000:
			press = str(display.data3['pressure'][0])[:4]
		elif display.data2['dewpoint'][0] < 1000:
			press = str(display.data3['pressure'][0])[:5]
		rpress = tinyfont.render(press + "Hg", True, lc)
		display.screen.blit(rpress, (400,84+50))
		rpress_label = tinyfont.render('Pressure:', True, lc)
		display.screen.blit(rpress_label, (317,84+50))
		
		volt = str(display.data3['voltage'][0])[:4]
		rvolt = tinyfont.render(volt + "vdc", True, lc)
		display.screen.blit(rvolt, (400,101+50))
		rvolt_label = tinyfont.render('Voltage:', True, lc)
		display.screen.blit(rvolt_label, (317,101+50))
		
		rssi = str(display.data3['rssi'][0])[:2]
		rrssi = tinyfont.render(rssi, True, lc)
		display.screen.blit(rrssi, (400,118+50))
		rrssi_label = tinyfont.render('RSSI:', True, lc)
		display.screen.blit(rrssi_label, (317,118+50))
		
		pygame.display.update()


if (1):
	d = SmDisplay()
	d.pickle_update()
	running = True
	disp0 = 0
	disp1 = 0
	disp2 = 0 
	disp3 = 0
	while running:
		try:
			while disp0 < 15:
				d.pickle_update()
				d.wx0_disp_update()
				disp0 +=1
				pygame.time.wait(1000)
			while disp1 < 15:
				d.pickle_update()
				d.wx1_disp_update()
				disp1 +=1
				pygame.time.wait(1000)
			while disp2 < 15:
				d.pickle_update()
				d.wx2_disp_update()
				disp2 +=1
				pygame.time.wait(1000)
			while disp3 < 15:
				d.pickle_update()
				d.wx3_disp_update()
				disp3 +=1
				pygame.time.wait(1000)
			disp0, disp1, disp2, disp3 = 0, 0, 0, 0
			continue
		except Exception:
			break
