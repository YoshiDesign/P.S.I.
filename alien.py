import pygame, os
from pygame.sprite import Sprite


class Alien(Sprite):

	# 0 = reg || 1 = twitter
	_current_game = 0
	
	def __init__(self, screen, g_settings):
		super(Alien, self).__init__()
		self.fp = os.fsencode("sprites/alien/")
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.g_settings = g_settings
		
		self.image = pygame.image.load(os.fsdecode(self.fp) + "a1_Alien.png")
		self.rect = self.image.get_rect()
		self.rect.x = self.rect.width 
		self.rect.y = self.rect.height

	@staticmethod
	def switch_game():
		Alien._current_game = 1
		
		
	def blitmeh(self):
		self.screen.blit(self.image, self.rect)
		
		
