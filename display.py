#/bin/python

import os, sys
import pygame
import time
from pygame.locals import *

black = (0,0,0)
white = (255,255,255)

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
		
		display.xmax = pygame.display.Info().current_w - 10
		display.ymax = pygame.display.Info().current_h - 5
		display.scaleicon = False
		display.iconscale = 1.0
		display.subwinTh = 0.065
		display.tmdateTh = 0.125
		display.tmdateSmTh = 0.09
		display.tmdateYPos = 1
		display.tmdateYPosSm = 8
	
	def display_update(display):
		display.screen.fill(black)
		xmin = 10
		xmax = display.xmax
		ymax = display.ymax
		fn = "freesans"
		lines = 5
		lc = (255,255,255)
		
		pygame.draw.line( display.screen, lc, (xmin,0),(xmax,0), lines ) #Top Line
		pygame.draw.line( display.screen, lc, (xmin,0),(xmin,ymax), lines ) #Left Line
		pygame.draw.line( display.screen, lc, (xmin,ymax),(xmax,ymax), lines ) #Bottom Line
		pygame.draw.line( display.screen, lc, (xmax,0),(xmax,ymax), lines ) #Right Line
		#pygame.draw.line( display.screen, lc, (xmin,ymax*0.15),(xmax,ymax*0.15), lines )
		#pygame.draw.line( display.screen, lc, (xmin,ymax*0.5),(xmax,ymax*0.5), lines )
		#pygame.draw.line( display.screen, lc, (xmax*0.25,ymax*0.5),(xmax*0.25,ymax), lines )
		#pygame.draw.line( display.screen, lc, (xmax*0.5,ymax*0.15),(xmax*0.5,ymax), lines )
		#pygame.draw.line( display.screen, lc, (xmax*0.75,ymax*0.5),(xmax*0.75,ymax), lines )
		
		th = display.tmdateTh
		sh = display.tmdateSmTh
		font = pygame.font.SysFont( fn, int(ymax*th), bold=1 )
		sfont = pygame.font.SysFont( fn, int(ymax*sh), bold=1 )
		
		tm1 = time.strftime( "%a, %b %d   %I:%M", time.localtime() )
		tm2 = time.strftime( "%S", time.localtime() )
		tm3 = time.strftime( " %P", time.localtime() )
		
		rtm1 = font.render( tm1, True, lc )
		(tx1,ty1) = rtm1.get_size()
		rtm2 = sfont.render( tm2, True, lc )
		(tx2,ty2) = rtm2.get_size()
		rtm3 = font.render( tm3, True, lc )
		(tx3,ty3) = rtm3.get_size()
		
		tp = xmax / 2 - (tx1 + tx2 + tx3) / 2
		display.screen.blit( rtm1, (tp+10,display.tmdateYPos) )
		display.screen.blit( rtm2, (tp+tx1+6,display.tmdateYPosSm) )
		display.screen.blit( rtm3, (tp+tx1+tx2,display.tmdateYPos) )
		
		pygame.display.update()


d = SmDisplay()
d.display_update()
s = time.localtime().tm_sec
while True:
	if s is not time.localtime().tm_sec:
		s = time.localtime().tm_sec
		d.display_update()
