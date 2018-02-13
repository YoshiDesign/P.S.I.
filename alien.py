import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	
	__mode = 0
	
	def __init__(self, screen, g_settings):
		super(Alien, self).__init__()
		
		self.screen = screen
		self.setting = g_settings
		

	@classmethod
	def hive_behavior(self, g_settings):
		# Theoretical
		pass
		
