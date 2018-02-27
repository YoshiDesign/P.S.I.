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
from entity.powerup import Powerups
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
	powerup = Powerups(g_settings)
	twits = Group()
	bullets = Group()

	# clock = pygame.time.Clock()
	# FPS = 31

	attack_twit_btn = Button(g_settings, screen, text="attk_twt", \
						 off_x=(g_settings.screen_width // 4))

	login_btn = Button(g_settings, screen, text="logins", \
				off_x=(g_settings.screen_width // 4) * -1, \
				off_y=(g_settings.screen_height // 8) * -1 )

	about_btn = Button(g_settings, screen, text="abut", \
						 off_x=(g_settings.screen_width // 4))

	to_pass_btn = Button(g_settings, screen, text="next", \
						 off_x=(g_settings.screen_width // 1))

	passed_btn = Button(g_settings, screen, text="nexted", \
						 off_x=(g_settings.screen_width // 1))


	""" KEYDOWNS occurring outside of gameplay compute within pygame_textinput.py for efficiency 
		When gameplay is active, textbox.update() ceases, and check_events takes over
	"""

	while True:

		# clock.tick(FPS)
		
		gf.update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
									twits, bullets, stats, scores, login_btn, \
									attack_twit_btn, about_btn, to_pass_btn, passed_btn)

		if stats.game_active == True:
			# As per the DocString
			gf.check_events(g_settings, screen, ship, aliens, stats, textbox, scores, twits, bullets)
			if stats._current_game:
				gf.update_twits(g_settings, screen, stats, ship, twits, scores, bullets)
				gf.update_bullets(g_settings, screen, stats, ship, scores, bullets, powerup, twits=twits)

		else:
			pass

if __name__ == "__main__":

	Main()
