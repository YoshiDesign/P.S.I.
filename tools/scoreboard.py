import pygame
from pygame.sprite import Group

from entity.ship import Ship

class Score():

	def __init__(self, g_settings, screen, stats):

		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.g_settings = g_settings
		self.stats = stats

		# Font
		self.white = (255,255,255)
		self.color2 = (255, 90, 90)
		self.font = pygame.font.SysFont(None, 48)
		self.font2 = pygame.font.SysFont(None, 32)

		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()


	def prep_ships(self):
		""" Track Lives """
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.screen, self.g_settings, self.stats)
			ship.rect.width -= 10
			ship.rect.x = self.screen_rect.centerx + ship_number * ship.rect.width
			ship.rect.y = 15
			self.ships.add(ship)

	def prep_score(self):

		score_str = "{:,}".format(self.stats.score)
		self.score_image = self.font.render(score_str, True, self.white, \
															 False)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 50
		self.score_rect.top = 12

	def prep_high_score(self):

		score_str = "High Score : {:,}".format(self.stats.high_score)
		self.high_score_image = self.font2.render(score_str, True, self.white, \
																  False)
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.bottom - 45

	def prep_level(self, up=0):
		""" Track Level """
		if up:
			self.stats.level += 1
		self.level_image = self.font2.render(str("Level " + str(self.stats.level)), \
													True, self.white, False)

		self.level_rect = self.level_image.get_rect()
		self.level_rect.left = self.screen_rect.left + 10
		self.level_rect.top = self.score_rect.top + 30

	def show_score(self):

		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)