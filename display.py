#/bin/python

import os, sys
import pygame
import time, datetime
import cPickle as pickle
import ephem
import traceback
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
		self.dateYPos = 3
		self.dateYPosSm = 10
	
	def __del___(self):
		'''DESTRUCTOR'''
	
	def pickle_data(self):
		try:
			location = '/home/pi/Power_Monitoring/'
			self.data = pickle.load(open(os.path.join(location, 'total_pickle.p'), "rb"))
		except Exception:
			print("ERROR: Pickle Update")
			traceback.print_exc(file=sys.stdout)
	
	def astro_data(self):
		try:
			cutty = ephem.Observer()
			cutty.lat = '41.42'
			cutty.long = '-70.92'
			cutty.elevation = 20
			dst_const = (ephem.hour * -4)
			self.d = {}
			planets = 	[ephem.Sun(),
					ephem.Moon(),
					ephem.Mars(),
					ephem.Jupiter(),
					ephem.Saturn(),
					ephem.Venus()]
			for o in planets:
				o.compute(cutty)
				if str(o.alt).startswith('-'):
					self.d[o.name] = {  'name'	: o.name,
							    'visible'	: False,
							    'altitude'	: o.alt,
							    'azimuth'	: o.az,
							    'rising'	: ephem.Date(cutty.next_rising(o) + dst_const),
							    'setting'	: ephem.Date(cutty.previous_setting(o) + dst_const)}
				else:
					self.d[o.name] = {  'name'	: o.name,
							    'visible'	: True,
							    'altitude'	: o.alt,
							    'azimuth'	: o.az,
							    'rising'	: ephem.Date(cutty.previous_rising(o) + dst_const),
							    'setting'	: ephem.Date(cutty.next_setting(o) + dst_const)}
		except Exception:
			print("ERROR: Ephem Update")
			traceback.print_exc(file=sys.stdout)
	
	def wx_disp(self, data):
		try:
			self.pickle_data()
			self.screen.fill(black)
			xmin = 10
			xmax = self.xmax
			ymax = self.ymax
			fn = "freesans"
			lines = 2
			lc = (255,255,255)
			################################################################################
			pygame.draw.line( self.screen, lc, (xmin,0),(xmax,0), lines) #Top Line
			pygame.draw.line( self.screen, lc, (xmin,0),(xmin,ymax), lines) #Left Line
			pygame.draw.line( self.screen, lc, (xmin,ymax),(xmax,ymax), lines) #Bottom Line
			pygame.draw.line( self.screen, lc, (xmax,0),(xmax,ymax), lines) #Right Line
			pygame.draw.line( self.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines) #Horizontal Line Under Top
			
			font = pygame.font.SysFont(fn, int(ymax*(self.txth)), bold=1 )
			tidefont = pygame.font.SysFont(fn, int(75), bold=1)
			lfont = pygame.font.SysFont(fn, int(135), bold=1)
			sfont = pygame.font.SysFont(fn, int(40), bold=1)
			smfont = pygame.font.SysFont(fn, int(25), bold=False)
			tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
			
			tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime())
			rtm1 = font.render(tm1, True, lc)
			self.screen.blit(rtm1, (30,self.dateYPos))
			
			icon_cutty = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/resources/', 'Cuttyhunk-Logo.png'))
			icon_cutty2 = pygame.transform.scale(icon_cutty, (62, 38))
			self.screen.blit(icon_cutty2, (395, 5))
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
			traceback.print_exc(file=sys.stdout)
	
	def tide_disp(self):
		try:
			self.pickle_data()
			self.screen.fill(black)
			xmin = 10
			xmax = self.xmax
			ymax = self.ymax
			fn = "freesans"
			lines = 2
			lc = (255,255,255)
			################################################################################
			pygame.draw.line( self.screen, lc, (xmin,0),(xmax,0), lines) #Top Line
			pygame.draw.line( self.screen, lc, (xmin,0),(xmin,ymax), lines) #Left Line
			pygame.draw.line( self.screen, lc, (xmin,ymax),(xmax,ymax), lines) #Bottom Line
			pygame.draw.line( self.screen, lc, (xmax,0),(xmax,ymax), lines) #Right Line
			pygame.draw.line( self.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines) #Horizontal Line Under Top
			
			font = pygame.font.SysFont(fn, int(ymax*(self.txth)), bold=1 )
			tidefont = pygame.font.SysFont(fn, int(75), bold=1)
			lfont = pygame.font.SysFont(fn, int(135), bold=1)
			sfont = pygame.font.SysFont(fn, int(40), bold=1)
			smfont = pygame.font.SysFont(fn, int(25), bold=False)
			tinyfont = pygame.font.SysFont(fn, int(16), bold=1)
			
			tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime())
			rtm1 = font.render(tm1, True, lc)
			self.screen.blit(rtm1, (30,self.dateYPos))
			
			icon_cutty = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/resources/', 'Cuttyhunk-Logo.png'))
			icon_cutty2 = pygame.transform.scale(icon_cutty, (62, 38))
			self.screen.blit(icon_cutty2, (395, 5))
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
			traceback.print_exc(file=sys.stdout)
	
	def astro_disp(self):
		try:
			self.astro_data()
			self.screen.fill(black)
			xmin = 10
			xmax = self.xmax
			ymax = self.ymax
			fn = "freesans"
			lines = 2
			lc = (255,255,255)
			################################################################################
			pygame.draw.line( self.screen, lc, (xmin,0),(xmax,0), lines) #Top Line
			pygame.draw.line( self.screen, lc, (xmin,0),(xmin,ymax), lines) #Left Line
			pygame.draw.line( self.screen, lc, (xmin,ymax),(xmax,ymax), lines) #Bottom Line
			pygame.draw.line( self.screen, lc, (xmax,0),(xmax,ymax), lines) #Right Line
			pygame.draw.line( self.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines) #Horizontal Line Under Top
			
			font = pygame.font.SysFont(fn, int(ymax*(self.txth)), bold=1 )
			tidefont = pygame.font.SysFont(fn, int(75), bold=1)
			lfont = pygame.font.SysFont(fn, int(135), bold=1)
			sfont = pygame.font.SysFont(fn, int(32), bold=1)
			snbfont = pygame.font.SysFont(fn, int(30), bold=False)
			smfont = pygame.font.SysFont(fn, int(19), bold=False)
			tinyfont = pygame.font.SysFont(fn, int(18), bold=1)
			
			tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime())
			rtm1 = font.render(tm1, True, lc)
			self.screen.blit(rtm1, (30,self.dateYPos))
			
			icon_cutty = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/resources/', 'Cuttyhunk-Logo.png'))
			icon_cutty2 = pygame.transform.scale(icon_cutty, (62, 38))
			self.screen.blit(icon_cutty2, (395, 5))
			################################################################################
			pygame.draw.line(self.screen, lc, (xmax*.5,ymax*.15),(xmax*.5,ymax), lines)
			
			sunname = self.d['Sun']['name']
			rsunname = font.render(sunname, True, lc)
			self.screen.blit(rsunname, (15, 47))
			
			alt = 'At:'
			ralt = tinyfont.render(alt, True, lc)
			self.screen.blit(ralt, (15, 82))
			sunalt = str(self.d['Sun']['altitude'])[:9]
			rsunalt = tinyfont.render(sunalt, True, lc)
			self.screen.blit(rsunalt, (40, 82))
			
			azm = 'Az:'
			razm = tinyfont.render(azm, True, lc)
			self.screen.blit(razm, (124, 82))
			sunazm = str(self.d['Sun']['azimuth'])[:9]
			rsunazm = tinyfont.render(sunazm, True, lc)
			self.screen.blit(rsunazm, (152, 82))
			
			pygame.draw.line(self.screen, lc, (xmin,213),(xmax*.5,213), lines)
			
			if self.d['Sun']['visible']:
				sunvis = '+'
				rsunvis = font.render(sunvis, True, lc)
				self.screen.blit(rsunvis, (210,40))
				
				sunrise = 'Rise:'
				rsunrise = smfont.render(sunrise, True, lc)
				self.screen.blit(rsunrise, (55, 90+17))
				
				sunrisetm = self.d['Sun']['rising'].datetime().strftime("%H:%M:%S")
				rsunrisetm = sfont.render(sunrisetm, True, lc)
				self.screen.blit(rsunrisetm, (107, 80+17))
				
				tmsunrise = str(datetime.datetime.now() - self.d['Sun']['rising'].datetime())[:8]
				rtmsunrise = snbfont.render(tmsunrise, True, lc)
				self.screen.blit(rtmsunrise, (107,108+17))
				
				sunset = 'Set:'
				rsunset = smfont.render(sunset, True, lc)
				self.screen.blit(rsunset, (55, 145+17))
				
				sunsettm = self.d['Sun']['setting'].datetime().strftime("%H:%M:%S")
				rsunsettm = sfont.render(sunsettm, True, lc)
				self.screen.blit(rsunsettm, (107, 135+17))
				
				tmsunset = str(self.d['Sun']['setting'].datetime() - datetime.datetime.now())[:8]
				rtmsunset = snbfont.render(tmsunset, True, lc)
				self.screen.blit(rtmsunset, (107, 163+17))
			else:
				sunvis = '-'
				rsunvis = font.render(sunvis, True, lc)
				self.screen.blit(rsunvis, (210,40))
				
				sunrise = 'Rise:'
				rsunrise = smfont.render(sunrise, True, lc)
				self.screen.blit(rsunrise, (55, 90+17))
				
				sunrisetm = self.d['Sun']['rising'].datetime().strftime("%H:%M:%S")
				rsunrisetm = sfont.render(sunrisetm, True, lc)
				self.screen.blit(rsunrisetm, (107, 80+17))
				
				tmsunrise = str(self.d['Sun']['rising'].datetime() - datetime.datetime.now())[:9]
				rtmsunrise = snbfont.render(tmsunrise, True, lc)
				self.screen.blit(rtmsunrise, (107,108+17))
				
				sunset = 'Set:'
				rsunset = smfont.render(sunset, True, lc)
				self.screen.blit(rsunset, (55, 145+17))
				
				sunsettm = self.d['Sun']['setting'].datetime().strftime("%H:%M:%S")
				rsunsettm = sfont.render(sunsettm, True, lc)
				self.screen.blit(rsunsettm, (107, 135+17))
				
				tmsunset = str(datetime.datetime.now() - self.d['Sun']['setting'].datetime())[:8]
				rtmsunset = snbfont.render(tmsunset, True, lc)
				self.screen.blit(rtmsunset, (107, 163+17))
			################################################################################
			moonname = self.d['Moon']['name']
			rmoonname = font.render(moonname, True, lc)
			self.screen.blit(rmoonname, (15, 215))
			
			malt = 'At:'
			moonalt = str(self.d['Moon']['altitude'])[:9]
			rmalt = tinyfont.render(malt + ' ' + moonalt, True, lc)
			self.screen.blit(rmalt, (15, 250))
			
			mazm = 'Az:'
			moonazm = str(self.d['Moon']['azimuth'])[:9]
			rmazm = tinyfont.render(mazm + ' ' + moonazm, True, lc)
			self.screen.blit(rmazm, (124, 250))
			if self.d['Moon']['visible']:
				moonvis = '+'
				rmoonvis = font.render(moonvis, True, lc)
				self.screen.blit(rmoonvis, (210,215))
				
				moonrise = 'Rise:'
				moonrisetm = self.d['Moon']['rising'].datetime().strftime("%H:%M:%S")
				tmmoonrise = str(datetime.datetime.now() - self.d['Moon']['rising'].datetime())[:8]
				rmoonrise = tinyfont.render(moonrise + ' ' + moonrisetm + ' ' + tmmoonrise, True, lc)
				self.screen.blit(rmoonrise, (15, 270))
				
				moonset = 'Set:'
				tmmoonset = str(self.d['Moon']['setting'].datetime() - datetime.datetime.now())[:8]
				moonsettm = self.d['Moon']['setting'].datetime().strftime("%H:%M:%S")
				rmoonset = tinyfont.render(moonset + '   ' + moonsettm + ' ' + tmmoonset, True, lc)
				self.screen.blit(rmoonset, (15, 290))
			else:
				moonvis = '-'
				rmoonvis = font.render(moonvis, True, lc)
				self.screen.blit(rmoonvis, (210,215))
				
				moonrise = 'Rise:'
				moonrisetm = self.d['Moon']['rising'].datetime().strftime("%H:%M:%S")
				tmmoonrise = str(self.d['Moon']['rising'].datetime() - datetime.datetime.now())[:9]
				rmoonrise = tinyfont.render(moonrise + ' ' + moonrisetm + ' ' + tmmoonrise, True, lc)
				self.screen.blit(rmoonrise, (15, 270))
				
				moonset = 'Set:'
				moonsettm = self.d['Moon']['setting'].datetime().strftime("%H:%M:%S")
				tmmoonset = str(datetime.datetime.now() - self.d['Moon']['setting'].datetime())[:8]
				rmoonset = tinyfont.render(moonset + '   ' + moonsettm + ' ' + tmmoonset, True, lc)
				self.screen.blit(rmoonset, (15, 290))
			################################################################################
			pygame.draw.line(self.screen, lc, (xmax*.5,(ymax*.15)+89),(xmax,(ymax*.15)+89), lines)
			pygame.draw.line(self.screen, lc, (xmax*.5,(ymax*.15)+(89*2)),(xmax,(ymax*.15)+(89*2)), lines)
			################################################################################
			marsname = self.d['Mars']['name']
			rmarsname = tinyfont.render(marsname, True, lc)
			self.screen.blit(rmarsname, (240, 45+10))
			
			mralt = 'At:'
			marsalt = str(self.d['Mars']['altitude'])[:9]
			rmralt = tinyfont.render(mralt + ' ' + marsalt, True, lc)
			self.screen.blit(rmralt, (240, 65+10))
			
			mrazm = 'Az:'
			marsazm = str(self.d['Mars']['azimuth'])[:9]
			rmrazm = tinyfont.render(mrazm + ' ' + marsazm, True, lc)
			self.screen.blit(rmrazm, (350, 65+10))
			if self.d['Mars']['visible']:
				marsvis = '+'
				rmarsvis = tinyfont.render(marsvis, True, lc)
				self.screen.blit(rmarsvis, (440,45+10))
				
				marsrise = 'Rise:'
				marsrisetm = self.d['Mars']['rising'].datetime().strftime("%H:%M:%S")
				tmmarsrise = str(datetime.datetime.now() - self.d['Mars']['rising'].datetime())[:8]
				rmarsrise = tinyfont.render(marsrise + ' ' + marsrisetm + ' ' + tmmarsrise, True, lc)
				self.screen.blit(rmarsrise, (240, 85+10))
				
				marsset = 'Set:'
				tmmarsset = str(self.d['Mars']['setting'].datetime() - datetime.datetime.now())[:8]
				marssettm = self.d['Mars']['setting'].datetime().strftime("%H:%M:%S")
				rmarsset = tinyfont.render(marsset + '   ' + marssettm + ' ' + tmmarsset, True, lc)
				self.screen.blit(rmarsset, (240, 105+10))
			else:
				marsvis = '-'
				rmarsvis = tinyfont.render(marsvis, True, lc)
				self.screen.blit(rmarsvis, (440,45+10))
				
				marsrise = 'Rise:'
				marsrisetm = self.d['Mars']['rising'].datetime().strftime("%H:%M:%S")
				tmmarsrise = str(self.d['Mars']['rising'].datetime() - datetime.datetime.now())[:9]
				rmarsrise = tinyfont.render(marsrise + ' ' + marsrisetm + ' ' + tmmarsrise, True, lc)
				self.screen.blit(rmarsrise, (240, 85+10))
				
				marsset = 'Set:'
				marssettm = self.d['Mars']['setting'].datetime().strftime("%H:%M:%S")
				tmmarsset = str(datetime.datetime.now() - self.d['Mars']['setting'].datetime())[:8]
				rmarsset = tinyfont.render(marsset + '   ' + marssettm + ' ' + tmmarsset, True, lc)
				self.screen.blit(rmarsset, (240, 105+10))
			################################################################################
			jname = self.d['Jupiter']['name']
			rjname = tinyfont.render(jname, True, lc)
			self.screen.blit(rjname, (240, 45+10+89))
			
			jalt = 'At:'
			jualt = str(self.d['Jupiter']['altitude'])[:9]
			rjalt = tinyfont.render(jalt + ' ' + jualt, True, lc)
			self.screen.blit(rjalt, (240, 65+10+89))
			
			jazm = 'Az:'
			juazm = str(self.d['Jupiter']['azimuth'])[:9]
			rjazm = tinyfont.render(jazm + ' ' + juazm, True, lc)
			self.screen.blit(rjazm, (350, 65+10+89))
			if self.d['Jupiter']['visible']:
				jvis = '+'
				rjvis = tinyfont.render(jvis, True, lc)
				self.screen.blit(rjvis, (440,45+10+89))
				
				jrise = 'Rise:'
				jrisetm = self.d['Jupiter']['rising'].datetime().strftime("%H:%M:%S")
				tmjrise = str(datetime.datetime.now() - self.d['Jupiter']['rising'].datetime())[:8]
				rjrise = tinyfont.render(jrise + ' ' + jrisetm + ' ' + tmjrise, True, lc)
				self.screen.blit(rjrise, (240, 85+10+89))
				
				jset = 'Set:'
				tmjset = str(self.d['Jupiter']['setting'].datetime() - datetime.datetime.now())[:8]
				jsettm = self.d['Jupiter']['setting'].datetime().strftime("%H:%M:%S")
				rjset = tinyfont.render(jset + '   ' + jsettm + ' ' + tmjset, True, lc)
				self.screen.blit(rjset, (240, 105+10+89))
			else:
				jvis = '-'
				rjvis = tinyfont.render(jvis, True, lc)
				self.screen.blit(rjvis, (440,45+10+89))
				
				jrise = 'Rise:'
				jrisetm = self.d['Jupiter']['rising'].datetime().strftime("%H:%M:%S")
				tmjrise = str(self.d['Jupiter']['rising'].datetime() - datetime.datetime.now())[:9]
				rjrise = tinyfont.render(jrise + ' ' + jrisetm + ' ' + tmjrise, True, lc)
				self.screen.blit(rjrise, (240, 85+10+89))
				
				jset = 'Set:'
				jsettm = self.d['Jupiter']['setting'].datetime().strftime("%H:%M:%S")
				tmjset = str(datetime.datetime.now() - self.d['Jupiter']['setting'].datetime())[:8]
				rjset = tinyfont.render(jset + '   ' + jsettm + ' ' + tmjset, True, lc)
				self.screen.blit(rjset, (240, 105+10+89))
			################################################################################
			sname = self.d['Saturn']['name']
			rsname = tinyfont.render(sname, True, lc)
			self.screen.blit(rsname, (240, 45+10+89+89))
			
			salt = 'At:'
			saalt = str(self.d['Saturn']['altitude'])[:9]
			rsalt = tinyfont.render(salt + ' ' + saalt, True, lc)
			self.screen.blit(rsalt, (240, 65+10+89+89))
			
			sazm = 'Az:'
			saazm = str(self.d['Saturn']['azimuth'])[:9]
			rsazm = tinyfont.render(sazm + ' ' + saazm, True, lc)
			self.screen.blit(rsazm, (350, 65+10+89+89))
			if self.d['Saturn']['visible']:
				svis = '+'
				rsvis = tinyfont.render(svis, True, lc)
				self.screen.blit(rsvis, (440,45+10+89+89))
				
				srise = 'Rise:'
				srisetm = self.d['Saturn']['rising'].datetime().strftime("%H:%M:%S")
				tmsrise = str(datetime.datetime.now() - self.d['Saturn']['rising'].datetime())[:8]
				rsrise = tinyfont.render(srise + ' ' + srisetm + ' ' + tmsrise, True, lc)
				self.screen.blit(rsrise, (240, 85+10+89+89))
				
				sset = 'Set:'
				tmsset = str(self.d['Saturn']['setting'].datetime() - datetime.datetime.now())[:8]
				ssettm = self.d['Saturn']['setting'].datetime().strftime("%H:%M:%S")
				rsset = tinyfont.render(sset + '   ' + ssettm + ' ' + tmsset, True, lc)
				self.screen.blit(rsset, (240, 105+10+89+89))
			else:
				svis = '-'
				rsvis = tinyfont.render(svis, True, lc)
				self.screen.blit(rsvis, (440,45+10+89+89))
				
				srise = 'Rise:'
				srisetm = self.d['Saturn']['rising'].datetime().strftime("%H:%M:%S")
				tmsrise = str(self.d['Saturn']['rising'].datetime() - datetime.datetime.now())[:9]
				rsrise = tinyfont.render(srise + ' ' + srisetm + ' ' + tmsrise, True, lc)
				self.screen.blit(rjrise, (240, 85+10+89+89))
				
				sset = 'Set:'
				ssettm = self.d['Saturn']['setting'].datetime().strftime("%H:%M:%S")
				tmsset = str(datetime.datetime.now() - self.d['Saturn']['setting'].datetime())[:8]
				rsset = tinyfont.render(sset + '   ' + ssettm + ' ' + tmsset, True, lc)
				self.screen.blit(rsset, (240, 105+10+89+89))
			################################################################################
			pygame.display.update()
			################################################################################
		except Exception:
			print("ERROR: ASTRO DISPLAY")
			traceback.print_exc(file=sys.stdout)

if (1):
	disp = SmDisplay()
	disp.astro_disp()
	running = True
	disp0, disp1, disp2, disp3, disp4, disp5 = 0, 0, 0, 0, 0, 0
	while running:
		while disp0 < 15:
			disp.wx_disp(0)
			disp0 +=1
			pygame.time.wait(1000)
		while disp1 < 15:
			disp.wx_disp(1)
			disp1 +=1
			pygame.time.wait(1000)
		while disp2 < 15:
			disp.wx_disp(2)
			disp2 +=1
			pygame.time.wait(1000)
		while disp3 < 15:
			disp.wx_disp(3)
			disp3 +=1
			pygame.time.wait(1000)
		while disp4 < 15:
			disp.tide_disp()
			disp4 += 1
			pygame.time.wait(1000)
		while disp5 < 30:
			disp.astro_disp()
			disp5 += 1
			pygame.time.wait(1000)
		if disp0 >= 15 and disp1 >= 15 and disp2 >= 15 and disp3 >= 15 and disp4 >= 15 and disp5 >= 30:
			disp0, disp1, disp2, disp3, disp4, disp5 = 0, 0, 0, 0, 0, 0
