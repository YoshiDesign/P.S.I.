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
		self.space = text_data["space"]

		# Determine Letter_Image to display
		if self.letter == "dots":

			self.filepath = os.fsencode(str("sprites/characters/ddd.png"))

		elif self.letter.isdigit():

			self.filepath = os.fsencode(str("sprites/characters/" + \
								"good" + str(self.letter) + ".png"))

		elif self.letter == "space":

			self.filepath = os.fsencode(str("sprites/characters/space.png"))

		elif self.sentiment == 1:

			self.filepath = os.fsencode(str("sprites/characters/" + \
								"good" + str(self.letter.upper()) + ".png"))
		else:
			self.filepath = os.fsencode(str("sprites/characters/" + \
								"bad" + str(self.letter.upper()) + ".png"))

		self.g_settings = g_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()		
		self.image = pygame.image.load(os.fsdecode(self.filepath))
		self.rect = self.image.get_rect()

		# Spacial props
		self.rect.y = self.rect.height
		self.rect.x = self.rect.width
		self.char_spacing = self.g_settings.char_spacing
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
		self.x += (self.g_settings.twit_speed * self.g_settings.twit_direction)
		self.rect.x = self.x

	def blitme(self, screen):
	 	self.screen.blit(self.image, self.rect)
