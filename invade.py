import sys
import pygame
from pygame.sprite import Group
from pygame.locals import *
import game_function as gf

from tools.scoreboard import Score
from pygame_textinput import TextInput
from tools.spritesheet import Spritesheet as sheet
from tools.statistic import Stats
from settings import Settings
from entity.explosion import Explosion
from entity.powerup import Powerup
from entity.buttons import Button
from entity.reticle import Reticle
from entity.alien import Alien
from entity.ship import Ship
from entity.tweeter import Tweeter

"""
	pygame.display.toggle_fullscreen
				  .set_icon
"""

def Main():
	
	pygame.init()
	pygame.display.set_caption("Personal Space")
	g_settings = Settings()
	screen = pygame.display.set_mode((g_settings.screen_width, \
										g_settings.screen_height))
	# Load the background image
	g_settings.load_background(screen)
	stats = Stats(g_settings)
	ship = Ship(screen, g_settings, stats)
	reticle = Reticle(g_settings, screen)
	textbox = TextInput()
	aliens = Alien(screen, g_settings)
	scores = Score(g_settings, screen, stats, ship)
	powerup = Powerup(g_settings)
	twits = Group()
	bullets = Group()
	# explode = Explosion(g_settings, screen)

	clock = pygame.time.Clock()
	FPS = 22

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

	while True:

		# clock.tick(FPS)
		
		
		clock.tick(FPS)
		gf.update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
									twits, bullets, stats, scores, buttons)


		if stats.game_active == True:
			# As per the DocString
			gf.check_events(g_settings, screen, ship, aliens, stats, textbox, scores, twits, bullets)
			if stats._current_screen == 3:
				gf.update_bullets(g_settings, screen, stats, ship, \
								scores, bullets, powerup, twits=twits)
				gf.update_twits(g_settings, screen, stats, ship, \
											twits, scores, bullets)

		else:
			pass


if __name__ == "__main__":

	Main()
