import pygame
from pygame.sprite import Sprite
import os
from analyze import Analyzer


# Could probably just add this to the alien.py file

class Tweeter(Sprite):
	_tweet = []
	_tweets_read = 0
	_total_twits_destroyed = 0
	
	def __init__(self, g_settings, screen, text_data={}):

		super(Tweeter, self).__init__()
		
		self.letter = text_data["letter"]
		self.sentiment = text_data["sentiment"]
		# Logical grouping
		self.twit_id = text_data["twit_id"]

		# Index within current characters on screen in order
		self.index = text_data["index"]
		self.twit_direction = 1
		self.health = g_settings.twit_hp
		self.power = 0

		# Determine Letter_Image to display
		if self.letter == "dots":
			self.filepath = os.fsencode(str("media/sprites/characters/ddd.png"))

		elif self.letter.isdigit():
			self.filepath = os.fsencode(str("media/sprites/characters/" + \
							"good" + str(self.letter) + ".png"))
		elif self.sentiment == 1:
			self.filepath = os.fsencode(str("media/sprites/characters/" + \
							"good" + str(self.letter.upper()) + ".png"))
		else:
			self.filepath = os.fsencode(str("media/sprites/characters/" + \
							"bad" + str(self.letter.upper()) + ".png"))

		self.g_settings = g_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()		
		self.image = pygame.image.load(os.fsdecode(self.filepath))
		self.rect = self.image.get_rect()

		# Spacial props // x and y are modified in gf.give_twit_dimension
		self.rect.y = self.rect.height
		self.rect.x = self.rect.width

		if self.letter.isdigit():
			self.char_spacing = 14
		else:
			self.char_spacing = self.g_settings.char_spacing

		self.x = float(self.rect.x)

	@staticmethod
	def level_up():
		self.g_settings.twit_hp += 33
		self.g_settings.twit_speed += 1.5


	def check_edges(self):
		# True if touching screen edge
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		else:
			return False

	def update(self):
		# Movement
		
		self.x += (self.g_settings.twit_speed * self.twit_direction)
		self.rect.x = self.x

	def blitme(self, screen):
	 	self.screen.blit(self.image, self.rect)
