import sys
import pygame
from pygame.sprite import Group
import game_function as gf
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
	
	g_settings = Settings()
	# Initialize Window
	screen = pygame.display.set_mode((g_settings.screen_width, g_settings.screen_height))
	pygame.display.set_caption("Personal Space")
	
	# Initialize Classes
	ship = Ship(screen, g_settings)
	testShip = Group()
	aliens = Group()
	#bullets = Group()
	
	


	while True:
		
		gf.check_events()
		
		gf.update_screen(g_settings, screen, ship)
		ship.update()


Main()
