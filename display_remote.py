#/bin/python

import os, sys
import pygame
import time, datetime
import cPickle as pickle
import ephem
import traceback
from pygame.locals import *
from standards import *

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
		exit(0)
	
	def pickle_data(self):
		try:
			subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "download", "/Programming/logs/cuttyhunk/total_pickle.p", "/home/pi/Power_Monitoring/output/"])
			location = '/home/pi/Power_Monitoring/output/'
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
	
	def astro_disp(self, data):
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
			tidefont = pygame.font.SysFont(fn, int(68), bold=1)
			lfont = pygame.font.SysFont(fn, int(62), bold=1)
			sfont = pygame.font.SysFont(fn, int(48), bold=1)
			snbfont = pygame.font.SysFont(fn, int(30), bold=False)
			snbfont1 = pygame.font.SysFont(fn, int(36), bold=False)
			smfont = pygame.font.SysFont(fn, int(26), bold=False)
			tinyfont = pygame.font.SysFont(fn, int(18), bold=1)
			
			tm1 = time.strftime("%a, %b %d %H:%M:%S", time.localtime())
			rtm1 = font.render(tm1, True, lc)
			self.screen.blit(rtm1, (30,self.dateYPos))
			
			icon_cutty = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/resources/', 'Cuttyhunk-Logo.png'))
			icon_cutty2 = pygame.transform.scale(icon_cutty, (62, 38))
			self.screen.blit(icon_cutty2, (395, 5))
			################################################################################
			icon_planet = pygame.image.load(os.path.join('/home/pi/Power_Monitoring/resources/', '%s.png' %data))
			icon_planet2 = pygame.transform.scale(icon_planet, (140, 140))
			self.screen.blit(icon_planet2, (310, 130))
			################################################################################
			name = self.d[data]['name']
			rname = tidefont.render(name, True, lc)
			self.screen.blit(rname, (15, 45))
			
			azmlabel = 'Azi:'
			azm = str(self.d[data]['azimuth'])[:9]
			razm = snbfont.render(azmlabel + azm, True, lc)
			self.screen.blit(razm, (270, 80))
			
			if self.d[data]['visible']:
				altlabel = 'Alt: '
				alt = str(self.d[data]['altitude'])[:8]
				ralt = snbfont.render(altlabel + alt, True, lc)
				self.screen.blit(ralt, (270, 50))
				
				rise = 'Rise:'
				rrise = smfont.render(rise, True, lc)
				self.screen.blit(rrise, (25, 133))
				
				risetm = self.d[data]['rising'].datetime().strftime("%H:%M:%S")
				rrisetm = sfont.render(risetm, True, lc)
				self.screen.blit(rrisetm, (100, 115))
				
				tmrise = str(datetime.datetime.now() - self.d[data]['rising'].datetime())[:8]
				rtmrise = snbfont1.render(tmrise, True, lc)
				self.screen.blit(rtmrise, (100,160))
				
				setlabel = 'Set:'
				rset = smfont.render(setlabel, True, lc)
				self.screen.blit(rset, (25, 228))
				
				settm = self.d[data]['setting'].datetime().strftime("%H:%M:%S")
				rsettm = sfont.render(settm, True, lc)
				self.screen.blit(rsettm, (100, 210))
				
				tmset = str(self.d[data]['setting'].datetime() - datetime.datetime.now())[:8]
				rtmset = snbfont1.render(tmset, True, lc)
				self.screen.blit(rtmset, (100, 160+95))
			else:
				altlabel = 'Alt: '
				alt = str(self.d[data]['altitude'])[:9]
				ralt = snbfont.render(altlabel + alt, True, lc)
				self.screen.blit(ralt, (270, 50))
				
				setlabel = 'Set:'
				rset = smfont.render(setlabel, True, lc)
				self.screen.blit(rset, (25, 133))
				
				settm = self.d[data]['setting'].datetime().strftime("%H:%M:%S")
				rsettm = sfont.render(settm, True, lc)
				self.screen.blit(rsettm, (100, 115))
				
				tmset = str(datetime.datetime.now() - self.d[data]['setting'].datetime())[:8]
				rtmset = snbfont1.render(tmset, True, lc)
				self.screen.blit(rtmset, (100, 160))
				
				rise = 'Rise:'
				rrise = smfont.render(rise, True, lc)
				self.screen.blit(rrise, (25, 228))
				
				risetm = self.d[data]['rising'].datetime().strftime("%H:%M:%S")
				rrisetm = sfont.render(risetm, True, lc)
				self.screen.blit(rrisetm, (100, 210))
				
				tmrise = str(self.d[data]['rising'].datetime() - datetime.datetime.now())[:9]
				rtmrise = snbfont1.render(tmrise, True, lc)
				self.screen.blit(rtmrise, (100,160+95))
			################################################################################
			pygame.display.update()
			################################################################################
		except Exception:
			print("ERROR: ASTRO DISPLAY")
			traceback.print_exc(file=sys.stdout)

if (1):
	disp = SmDisplay()
	running = True
	tide_data = True
	delay = {'Weather'	: 10,
		 'Tide'		: 15,
		 'Astronomy'	: 10}
	wx_d = [0,1,2,3,4,5,6]
	as_d = ['Sun', 'Moon', 'Venus', 'Mars', 'Jupiter', 'Saturn']
	while running:		
		try:
			for s in wx_d:
				counter = 0
				while counter < delay['Weather']:
					disp.wx_disp(s)
					pygame.time.wait(1000)
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
							counter = 500
							break
					counter += 1
				pass
			if tide_data:
				counter = 0
				while counter < delay['Tide']:
					disp.tide_disp()
					pygame.time.wait(1000)
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
							counter = 500
							break
					counter += 1
				pass
			for s in as_d:
				counter = 0
				while counter < delay['Astronomy']:
					disp.astro_disp(s)
					pygame.time.wait(1000)
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
							counter = 500
							break
					counter += 1
				pass
					
		except KeyboardInterrupt:
    			running = False
			print('interrupted!')
