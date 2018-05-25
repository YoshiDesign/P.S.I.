import sys
import pygame
import requests
from time import sleep
from pygame.locals import *
from pygame.sprite import Group
from multiprocessing import Process, Pipe, Queue

import game_function as gf
from tools.scoreboard import Score
from pygame_textinput import TextInput
from tools.spritesheet import Spritesheet as sheet
from tools.statistic import Stats
from settings import Settings
from entity.explosion import Explosion
from entity.buttons import Button
from entity.reticle import Reticle
from entity.alien import Alien
from entity.ship import Ship
from entity.tweeter import Tweeter

"""
	pygame.display.toggle_fullscreen
				  .set_icon
"""

def Main(enter, exit):
	
	# Run main // (enter, exit) are not used to track exit conditions
	pygame.init()
	pygame.display.set_caption("PSI")
	g_settings 	= Settings(exit)
	screen 		= pygame.display.set_mode((g_settings.screen_width, \
										g_settings.screen_height))
	font 		= pygame.font.SysFont(None, 48)
	g_settings.load_background(screen)

	stats 		= Stats(g_settings)
	ship 		= Ship(screen, g_settings, stats)
	reticle 	= Reticle(g_settings, screen)
	textbox 	= TextInput()
	aliens 		= Alien(screen, g_settings)
	scores 		= Score(g_settings, screen, stats, ship)
	powerups 	= Group()
	twits 		= Group()

	# wpns
	bullets = Group()
	lazers 	= Group()
	bombs 	= Group()

	# Our weapons
	projectiles = [bombs, bullets, lazers]
	# btns
	attack_btn 	= Button(g_settings, screen, [527, 400, 159, 50], 2)
	login_btn 	= Button(g_settings, screen, [130, 258, 220, 50], 2)
	about_btn	= Button(g_settings, screen, [820, 260, 245, 50], 2)
	pass_btn 	= Button(g_settings, screen, [550, 342, 100, 37], 2)
	passed_btn 	= Button(g_settings, screen, [540, 342, 122, 37], 2)

	# Our buttons
	buttons 	= [login_btn, about_btn, attack_btn, pass_btn, passed_btn]
	clock 		= pygame.time.Clock()
	FPS 		= 22

	""" 
		KEYDOWNS occurring outside of gameplay compute within pygame_textinput.py 
		When game is active, textbox.update() ceases, and gf.check_events takes over.
	"""

	while True: # Main Game Loop loops

		clock.tick(FPS)
		
		if gf.update_screen(g_settings, screen, font, ship, textbox, aliens, reticle, \
												twits, powerups, projectiles, stats, \
														scores, buttons) == 'TX_QUIT':
			# If we receive the quit flag.
			return True

		if stats.game_active == True:
			#enter.send('hello')
			# As per the DocString
			if gf.check_events(g_settings, screen, ship, aliens, stats, \
										scores, projectiles) == 'CE_QUIT':
				# if we receive the quit flag
				return True
			if stats._current_screen == 3:

				gf.update_bullets(g_settings, screen, stats, ship, \
									scores, projectiles, powerups, \
											enter, exit, twits=twits)

				gf.update_twits(g_settings, screen, stats, ship, powerups,\
												twits, scores, projectiles)
				
if __name__ == "__main__":

	# P's & Queue
	enter, exit = Pipe()
	q = Queue()

	# This runs the game, all parts tied together by signals CE_ and TX_
	main_program_ends = Main(enter, exit)
	
	# Ritardando
	if main_program_ends:

		sys.exit()

