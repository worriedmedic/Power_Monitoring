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
	def __init__(self):
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
		self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.screen.fill(black)
		pygame.font.init()
		pygame.mouse.set_visible(0)
		pygame.display.update()
		
		self.icon = [ 0, 0, 0, 0 ]
		
		self.xmax = pygame.display.Info().current_w - 10
		self.ymax = pygame.display.Info().current_h - 6
		self.scaleicon = False
		self.iconscale = 1.0
		self.subwinTh = 0.065
		self.txth = 0.115
		self.lrgtxth = 0.4
		self.smtxth = 0.1
		self.smrtxth = 0.065
		self.tinytxth = 0.04
		self.dateYPos = 1
		self.dateYPosSm = 8
	
	def __del___(self):
		'''DESTRUCTOR'''
	
	def pickle_update(self):
		try:
			location = '/home/pi/Power_Monitoring/pickle/'
			self.data = pickle.load(open('total_pickle.p', "rb"))
		except Exception:
			print("ERROR: Pickle Update")
	
	def wx_disp(self, data):
		try:
			self.screen.fill(black)
			xmin = 10
			xmax = self.xmax
			ymax = self.ymax
			fn = "freesans"
			lines = 2
			lc = (255,255,255)
			
			################################################################################
			pygame.draw.line( self.screen, lc, (xmin,0),(xmax,0), lines ) #Top Line
			pygame.draw.line( self.screen, lc, (xmin,0),(xmin,ymax), lines ) #Left Line
			pygame.draw.line( self.screen, lc, (xmin,ymax),(xmax,ymax), lines ) #Bottom Line
			pygame.draw.line( self.screen, lc, (xmax,0),(xmax,ymax), lines ) #Right Line
			pygame.draw.line( self.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines ) #Horizontal Line Under Top
			
			font = pygame.font.SysFont( fn, int(ymax*(self.txth)), bold=1 )
			lfont = pygame.font.SysFont( fn, int(135), bold=1 )
			sfont = pygame.font.SysFont( fn, int(ymax*(self.smtxth)), bold=1 )
			smfont = pygame.font.SysFont(fn, int(ymax*(self.smrtxth)), bold=1)
			tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
			
			tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
			
			rtm1 = font.render(tm1, True, lc)
			
			self.screen.blit(rtm1, (15,self.dateYPos))
			
			weather_data = {'sunrise'	: self.data[8]['sunrise'],
					'sunset'	: self.data[8]['sunset']}
			
			sunrise = smfont.render(weather_data['sunrise'], True, lc)
			(srx1, sry1) = sunrise.get_size()
			sunset = smfont.render(weather_data['sunset'], True, lc)
			(ssx1, ssy1) = sunset.get_size()
			
			self.screen.blit(sunrise, (428,2))
			self.screen.blit(sunset, (417,20))
			################################################################################
			pygame.draw.line(self.screen, lc, (310,ymax*0.15),(310,ymax*0.6), lines) #Vertical Line @x:310
			pygame.draw.line(self.screen, lc, (xmin,ymax*0.6),(xmax,ymax*0.6), lines)
			
			if self.data[data]['temperature'][0] < 100:
				temp = str(self.data[data]['temperature'][0])[:4]
			elif self.data[data]['temperature'][0] >= 100:
				temp = str(self.data[data]['temperature'][0])[:3]
			rtemp = lfont.render(temp, True, lc)
			self.screen.blit(rtemp, (18, 32))
			
			rsensorlabel = font.render(self.data[data]['name'][:7], True, lc)
			self.screen.blit(rsensorlabel, (317,50))
			
			dfont = pygame.font.SysFont(fn, int(40), bold=1 )
			dtxt = dfont.render(uniTmp, True, lc )
			self.screen.blit(dtxt, (270, 50))
			
			rtemptime = tinyfont.render(self.data[data]['time'].strftime("%y-%m-%d %H:%M:%S"), True, lc)
			self.screen.blit(rtemptime, (15, 165))
			
			rtempmax = tinyfont.render('Max: ' + str(self.data[data]['temperature_max'])[:4], True, lc)
			self.screen.blit(rtempmax, (162, 165))
			
			rtempmin = tinyfont.render('Min: ' + str(self.data[data]['temperature_min'])[:4], True, lc)
			self.screen.blit(rtempmin, (238, 165))
			################################################################################
			tempgraph = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/output/', 'plot_sm_Temperature_sensor_%s.png' %data))
			tempgraph2 = pygame.transform.scale(tempgraph, (455, 122))
			self.screen.blit(tempgraph2, (12,192))
			################################################################################
			if self.data[data]['humidity'][0] == 100:
				humid = str(self.data[data]['humidity'][0])[:3]
			elif self.data[data]['humidity'][0] < 100:
				humid = str(self.data[data]['humidity'][0])[:4]
			rhumid = tinyfont.render(humid + '%', True, lc)
			self.screen.blit(rhumid, (400, 50+50))
			rhumid_label = tinyfont.render('Humid:', True, lc)
			self.screen.blit(rhumid_label, (317, 50+50))
			
			if self.data[data]['dewpoint'][0] == 100:
				dew = str(self.data[data]['dewpoint'][0])[:3]
			elif self.data[data]['dewpoint'][0] < 100:
				dew = str(self.data[data]['dewpoint'][0])[:4]
			rdew = tinyfont.render(dew + " " + uniTmp, True, lc)
			self.screen.blit(rdew, (400,67+50))
			rdew_label = tinyfont.render('Dewpoint:', True, lc)
			self.screen.blit(rdew_label, (317,67+50))
			
			if self.data[data]['pressure'][0] >= 1000:
				press = str(self.data[data]['pressure'][0])[:4]
			elif self.data[data]['dewpoint'][0] < 1000:
				press = str(self.data[data]['pressure'][0])[:5]
			rpress = tinyfont.render(press + "Hg", True, lc)
			self.screen.blit(rpress, (400,84+50))
			rpress_label = tinyfont.render('Pressure:', True, lc)
			self.screen.blit(rpress_label, (317,84+50))
			
			volt = str(self.data[data]['voltage'][0])[:4]
			rvolt = tinyfont.render(volt + "vdc", True, lc)
			self.screen.blit(rvolt, (400,101+50))
			rvolt_label = tinyfont.render('Voltage:', True, lc)
			self.screen.blit(rvolt_label, (317,101+50))
			
			rssi = str(self.data[data]['rssi'][0])[:2]
			rrssi = tinyfont.render(rssi, True, lc)
			self.screen.blit(rrssi, (400,118+50))
			rrssi_label = tinyfont.render('RSSI:', True, lc)
			self.screen.blit(rrssi_label, (317,118+50))
			
			################################################################################
			pygame.display.update()
			################################################################################
		except Exception:
			print('ERROR: WX DISPLAY')
	
	def tide_disp(self):
		try:
			self.screen.fill(black)
			xmin = 10
			xmax = self.xmax
			ymax = self.ymax
			fn = "freesans"
			lines = 2
			lc = (255,255,255)
			
			################################################################################
			pygame.draw.line( self.screen, lc, (xmin,0),(xmax,0), lines ) #Top Line
			pygame.draw.line( self.screen, lc, (xmin,0),(xmin,ymax), lines ) #Left Line
			pygame.draw.line( self.screen, lc, (xmin,ymax),(xmax,ymax), lines ) #Bottom Line
			pygame.draw.line( self.screen, lc, (xmax,0),(xmax,ymax), lines ) #Right Line
			pygame.draw.line( self.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines ) #Horizontal Line Under Top
			
			font = pygame.font.SysFont(fn, int(ymax*(self.txth)), bold=1 )
			tidefont = pygame.font.SysFont(fn, int(75), bold=1 )
			lfont = pygame.font.SysFont(fn, int(135), bold=1 )
			sfont = pygame.font.SysFont(fn, int(40), bold=1 )
			smfont = pygame.font.SysFont(fn, int(ymax*(self.smrtxth)), bold=1)
			tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
			
			tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime() )
			
			rtm1 = font.render(tm1, True, lc)
			
			self.screen.blit(rtm1, (15,self.dateYPos))
			
			weather_data = {'sunrise'	: self.data[8]['sunrise'],
					'sunset'	: self.data[8]['sunset']}
			
			sunrise = smfont.render(weather_data['sunrise'], True, lc)
			(srx1, sry1) = sunrise.get_size()
			sunset = smfont.render(weather_data['sunset'], True, lc)
			(ssx1, ssy1) = sunset.get_size()
			
			self.screen.blit(sunrise, (428,2))
			self.screen.blit(sunset, (417,20))
			################################################################################
			tide_title = tidefont.render('Tides', True, lc)
			self.screen.blit(tide_title, (20, 50))
			
			icon_tide = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/resources/', 'tide.png'))
			icon_tide_2 = pygame.transform.scale(icon_tide, (155, 85))
			self.screen.blit(icon_tide_2, (275, 60))
			
			td_pr_yh = 150
			rtd_pr = tinyfont.render('Tide Prior', True, lc)
			self.screen.blit(rtd_pr, (20, td_pr_yh - 15))
			rtd_pr_tm = sfont.render(str(self.data[9]['tide_prior_time'].strftime("%H:%M")), True, lc)
			self.screen.blit(rtd_pr_tm, (20, td_pr_yh))
			rtd_pr_ty = sfont.render(self.data[9]['tide_prior_type'], True, lc)
			self.screen.blit(rtd_pr_ty, (140, td_pr_yh))
			rtd_pr_lv = sfont.render(str(self.data[9]['tide_prior_level'])[:4], True, lc)
			self.screen.blit(rtd_pr_lv, (220, td_pr_yh))
			td_pr_cn = datetime.datetime.now() - self.data[9]['tide_prior_time']
			rtd_pr_cn = sfont.render(str(td_pr_cn)[:7], True, lc)
			self.screen.blit(rtd_pr_cn, (320, td_pr_yh))
			
			td_nx_yh = 150 + 60
			rtd_nx = tinyfont.render('Tide Next', True, lc)
			self.screen.blit(rtd_nx, (20, td_nx_yh - 15))
			rtd_nx_tm = sfont.render(str(self.data[9]['tide_next_time'].strftime("%H:%M")), True, lc)
			self.screen.blit(rtd_nx_tm, (20, td_nx_yh))
			rtd_nx_ty = sfont.render(self.data[9]['tide_next_type'], True, lc)
			self.screen.blit(rtd_nx_ty, (140, td_nx_yh))
			rtd_nx_lv = sfont.render(str(self.data[9]['tide_next_level'])[:4], True, lc)
			self.screen.blit(rtd_nx_lv, (220, td_nx_yh))
			td_nx_cn = self.data[9]['tide_next_time'] - datetime.datetime.now()
			rtd_nx_cn = sfont.render(str(td_nx_cn)[:7], True, lc)
			self.screen.blit(rtd_nx_cn, (320, td_nx_yh))
			
			td_af_yh = 150 + 120
			rtd_af = tinyfont.render('Tide Next', True, lc)
			self.screen.blit(rtd_af, (20, td_af_yh - 15))
			rtd_af_tm = sfont.render(str(self.data[9]['tide_after_time'].strftime("%H:%M")), True, lc)
			self.screen.blit(rtd_af_tm, (20, td_af_yh))
			rtd_af_ty = sfont.render(self.data[9]['tide_after_type'], True, lc)
			self.screen.blit(rtd_af_ty, (140, td_af_yh))
			rtd_af_lv = sfont.render(str(self.data[9]['tide_after_level'])[:4], True, lc)
			self.screen.blit(rtd_af_lv, (220, td_af_yh))
			td_af_cn = self.data[9]['tide_after_time'] - datetime.datetime.now()
			rtd_af_cn = sfont.render(str(td_af_cn)[:7], True, lc)
			self.screen.blit(rtd_af_cn, (320, td_af_yh))
			################################################################################
			pygame.display.update()
			################################################################################
		except Exception:
			print("ERROR: TIDE DISPLAY")

if (1):
	d = SmDisplay()
	d.pickle_update()
	d.tide_disp()
	running = True
	disp0, disp1, disp2, disp3, disp4 = 0, 0, 0, 0, 0
	while running:
		while disp0 < 15:
			d.pickle_update()
			d.wx_disp(0)
			disp0 +=1
			pygame.time.wait(1000)
		while disp1 < 15:
			d.pickle_update()
			d.wx_disp(1)
			disp1 +=1
			pygame.time.wait(1000)
		while disp2 < 15:
			d.pickle_update()
			d.wx_disp(2)
			disp2 +=1
			pygame.time.wait(1000)
		while disp3 < 15:
			d.pickle_update()
			d.wx_disp(3)
			disp3 +=1
			pygame.time.wait(1000)
		while disp4 < 15:
			d.pickle_update()
			d.tide_disp()
			disp4 += 1
			pygame.time.wait(1000)
		if disp0 >= 15 and disp1 >= 15 and disp2 >= 15 and disp3 >= 15 and disp4 >= 15:
			disp0, disp1, disp2, disp3, disp4 = 0, 0, 0, 0, 0
