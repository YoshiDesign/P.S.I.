""" 
	OPTS:
	lives - does not need its own module

""" 


import sys
import pygame
from time import sleep
from pygame.locals import *
from pygame.sprite import Group
from multiprocessing import Process, Pipe, Queue, set_start_method

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

def generate_field(i, q=0):

	""" 
		Simple reverse generator 
		Allows for optional additions 
		to extend prolong from StopIteration
	"""
	if q:
		i = i + q

	for x in range(i, 0, -1):
		try:
			yield x
		except StopIteration:
			pass


def listening(flag, enter, exit):

	""" A Target of Multiprocess """

	wait_time = float(0.01)

	while True:

		data = exit.recv()
		# For your health
		if data:

			print("FOUND DATA")
			print(data)

			if data['power'] == 'bulletup':

				pygame.draw.rect()

			if data['power'] == 'bombup':
				pass
			if data['power'] == 'lazerup':
				pass

				
		sleep(wait_time)


def Main(enter, exit, screen, g_settings):
	
	
	# Load the background image
	g_settings.load_background(screen)
	stats = Stats(g_settings)
	ship = Ship(screen, g_settings, stats)
	reticle = Reticle(g_settings, screen)
	textbox = TextInput()
	aliens = Alien(screen, g_settings)
	scores = Score(g_settings, screen, stats, ship)
	powerups = Group()
	twits = Group()
	bullets = Group()
	# explode = Explosion(g_settings, screen)

	clock = pygame.time.Clock()
	FPS = 22
	switch = 0

	attack_btn = Button(g_settings, screen, [527, 400, 159, 50], 2)
	login_btn = Button(g_settings, screen, [130, 258, 220, 50], 2)
	about_btn = Button(g_settings, screen, [820, 260, 245, 50], 2)
	pass_btn = Button(g_settings, screen, [550, 342, 100, 37], 2)
	passed_btn = Button(g_settings, screen, [540, 342, 122, 37], 2)

	buttons = [login_btn, about_btn, attack_btn, pass_btn, passed_btn]


	""" 
		KEYDOWNS occurring outside of gameplay compute within pygame_textinput.py for efficiency 
		When gameplay is active, textbox.update() ceases, and check_events takes over
	"""

	while True: # Main Game Loop loops

		clock.tick(FPS)

		if gf.update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
												twits, powerups, bullets, stats, \
												scores, buttons) == 'TX_QUIT':
			# If we receive the quit flag.
			return True

		if stats.game_active == True:
			#enter.send('hello')
			# As per the DocString
			if gf.check_events(g_settings, screen, ship, aliens, stats, \
									scores, twits, bullets) == 'CE_QUIT':
				# if we receive the quit flag
				return True
			if stats._current_screen == 3:

				gf.update_bullets(g_settings, screen, stats, ship, \
								scores, bullets, powerups, enter, exit, twits=twits)
				gf.update_twits(g_settings, screen, stats, ship, powerups,\
											twits, scores, bullets)

if __name__ == "__main__":

	q = Queue()
	enter, exit = Pipe()
	listener = Process(target=listening, args=(1, enter, exit))
	listener.start()

	# Run main // (enter, exit) are not used to track exit conditions
	pygame.init()
	pygame.display.set_caption("Personal Space")
	g_settings = Settings()
	screen = pygame.display.set_mode((g_settings.screen_width, \
										g_settings.screen_height))
	main_program_ends = Main(enter, exit, screen, g_settings)

	if main_program_ends:
		listener.terminate()
		sys.exit()

