import sys
import pygame
from pygame.sprite import Group
from pygame.locals import *
import game_function as gf

from tools.scoreboard import Score
from tools.pygame_textinput import TextInput
from tools.spritesheet import Spritesheet as sheet
from tools.statistic import Stats
from settings import Settings
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
	scores = Score(g_settings, screen, stats)
	twits = Group()
	bullets = Group()

	clock = pygame.time.Clock()
	FPS = 31

	play_twit_btn = Button(g_settings, screen, text="Tweets", \
						 off_x=(g_settings.screen_width // 4))

	play_reg_btn = Button(g_settings, screen, text="PLAY", \
				off_x=(g_settings.screen_width // 4) * -1, \
				off_y=(g_settings.screen_height // 8) * -1 )

	while True:

		clock.tick(FPS)

		gf.update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
						twits, bullets, stats, scores, play_reg_btn, play_twit_btn)

		gf.check_events(g_settings, screen, ship, aliens, stats, textbox, \
										twits, bullets, play_twit_btn, play_reg_btn)

		if stats.game_active == True:
			if stats._current_game:
				gf.update_twits(g_settings, screen, stats, ship, twits, scores, bullets)
				gf.update_bullets(g_settings, screen, stats, ship, twits, scores, bullets)

			# gf.update_twits(g_settings, screen, stats, ship, twits)



		

if __name__ == "__main__":

	Main()
