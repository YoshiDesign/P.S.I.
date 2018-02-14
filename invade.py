import sys
import pygame
from pygame.sprite import Group
from pygame.locals import *
import game_function as gf
from spritesheet import Spritesheet as sheet
from statistic import Stats
from settings import Settings
from buttons import Button
from alien import Alien
from ship import Ship

"""
	pygame.display.toggle_fullscreen
				  .set_icon
"""




def Main():
	
	pygame.init()
	CLOCK = pygame.time.Clock()
	print("CLOCK == ".format(CLOCK))
	FPS = 10
	g_settings = Settings()
	# Initialize Window
	screen = pygame.display.set_mode((g_settings.screen_width, g_settings.screen_height))
	g_settings.load_background(screen)
	
	pygame.display.set_caption("Personal Space")
	
	HW, HH = g_settings.screen_width / 2, g_settings.screen_height / 2
	
	# Initialize Classes
	stats = Stats(g_settings)
	ship = Ship(screen, g_settings)
	testShip = Group()
	aliens = Group()
	#bullets = Group()
	
	gf.start_game(g_settings, screen, stats)
	print(stats.game_active)
	index = 0
	
	while True:
		
		gf.check_events(g_settings, screen, ship, stats)
		gf.update_screen(g_settings, screen, ship)


Main()
