import sys
import pygame
from pygame_textinput import TextInput
from pygame.sprite import Group
from pygame.locals import *
import game_function as gf
from spritesheet import Spritesheet as sheet
from statistic import Stats
from settings import Settings
from buttons import Button
from reticle import Reticle
from alien import Alien
from ship import Ship

"""
	pygame.display.toggle_fullscreen
				  .set_icon
"""



def Main():
	
	pygame.init()
	pygame.display.set_caption("Personal Space")

	g_settings = Settings()
	screen = pygame.display.set_mode((g_settings.screen_width, g_settings.screen_height))
	
	g_settings.load_background(screen)
	stats = Stats(g_settings)
	ship = Ship(screen, g_settings)
	ret = Reticle(g_settings, screen)
	textbox = TextInput()
	aliens = Alien(screen, g_settings)
	#bullets = Group()
	
	print(stats.game_active)	
	while True:

		gf.update_screen(g_settings, screen, ship, aliens, ret, stats)

		# Separation of concerns is necessary to implement textbox

		if stats.game_active:
			gf.start_game(g_settings, screen, ship, stats)
			gf.check_events(g_settings, screen, ship, stats)

		else:

			
				
		### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
			# Gather Textbox resources & set to screen
			gf.get_infoz(g_settings, screen, ship, stats, textbox)
				
			

		### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

		
			# screen.blit(textbox.get_surface(),(10,10))
		
		pygame.display.flip()


			

if __name__ == "__main__":

	Main()
