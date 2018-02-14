import pygame, os
from pygame.sprite import Sprite


class Alien(Sprite):
	
	def __init__(self, screen, g_settings):
		super(Alien, self).__init__()
		self.fp = os.fsencode("sprites/alien/")
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.setting = g_settings
		
		self.image = pygame.image.load(os.fsdecode(self.fp) + "a1_Alien.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = self.screen_rect.centerx
		self.rect.top = self.screen_rect.centery + 20
		

	#~ @classmethod
	#~ def hive_behavior(self, g_settings):
		#~ # Theoretical
		#~ pass
		
	def blitmeh(self):
		self.screen.blit(self.image, self.rect)
		
		
