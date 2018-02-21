import pygame
from random import randint

class Powerups():

	def __init__(self, g_settings):

		self.g_settings = g_settings
		
		


	def spawn_powerup(self, twit):

		if not randint(1,11) % 3:

			return True
		else:
			return False
