#/bin/python

import os, sys
import pygame
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
		display.tmdateSmTh = 0.075
		display.tmdateYPos = 1
		display.tmdateYosSm = 8
	
	def display_update(display):
		display.screen.fill(black)
		xmin = 10
		xmax = display.xmax
		ymax = display.ymax
		fn = "freesans"
		lines = 5
		white = (255,255,255)
		
		pygame.draw.line( display.screen, white, (xmin,0),(xmax,0), lines )
		pygame.draw.line( display.screen, white, (xmin,0),(xmin,ymax), lines )
		pygame.draw.line( display.screen, white, (xmin,ymax),(xmax,ymax), lines )
		pygame.draw.line( display.screen, white, (xmax,0),(xmax,ymax+2), lines )
		pygame.draw.line( display.screen, white, (xmin,ymax*0.15),(xmax,ymax*0.15), lines )
		pygame.draw.line( display.screen, white, (xmin,ymax*0.5),(xmax,ymax*0.5), lines )
		pygame.draw.line( display.screen, white, (xmax*0.25,ymax*0.5),(xmax*0.25,ymax), lines )
		pygame.draw.line( display.screen, white, (xmax*0.5,ymax*0.15),(xmax*0.5,ymax), lines )
		pygame.draw.line( display.screen, white, (xmax*0.75,ymax*0.5),(xmax*0.75,ymax), lines )
		
	
