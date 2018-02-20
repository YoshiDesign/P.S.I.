import pygame
from pygame.sprite import Sprite
from collections import OrderedDict as OD
import os
from analyze import Analyzer


# Could probably just add this to the alien.py file

class Tweeter(Sprite):
	_tweet = []
	_tweets_read = 0
	# Good or bad -- for debuggin'
	_total_twits = 0
	# (... sentiment=1...) infers positive by default
	def __init__(self, g_settings, screen, text_data={}):
		Tweeter._total_twits += 1
		super(Tweeter, self).__init__()
		self.text_data = text_data
		self.letter = text_data["letter"]
		self.sentiment = text_data["sentiment"]

		# Determine character to display
		# self.space is repetative for readability
		if self.letter == "dots":

			self.filepath = os.fsencode(str("sprites/characters/ddd.png"))
			self.space = False

		elif self.letter.isdigit():

			self.filepath = os.fsencode(str("sprites/characters/" + \
								"good" + str(self.letter) + ".png"))
			self.space = False

		elif self.letter == "space":

			self.filepath = os.fsencode(str("sprites/characters/space.png"))
			self.space = True

		elif self.sentiment == 1:

			self.filepath = os.fsencode(str("sprites/characters/" + \
								"good" + str(self.letter.upper()) + ".png"))
			self.space = False
		else:
			self.filepath = os.fsencode(str("sprites/characters/" + \
								"bad" + str(self.letter.upper()) + ".png"))
			self.space = False

		self.g_settings = g_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()		
		self.image = pygame.image.load(os.fsdecode(self.filepath))
		self.rect = self.image.get_rect()
		# Dimensions
		self.rect.y = self.rect.height
		self.rect.x = self.rect.width
		self.char_spacing = self.g_settings.char_spacing
		# For more granular horizontal movement
		self.x = float(self.rect.x)


	def check_edges(self):
		# True if touching
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		else:
			# moot
			return False

	def update(self):
		# Movement
		self.x += (self.g_settings.twit_drop_speed *\
				self.g_settings.twit_direction)
		self.rect.x = self.x

	def blitme(self, screen):
	 	self.screen.blit(self.image, self.rect)
