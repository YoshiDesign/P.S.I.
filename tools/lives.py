import os
import pygame
from pygame.sprite import Sprite

class Life(Sprite):

	def __init__(self, g_settings, screen):

		super(Life, self).__init__()

		self.life = os.fsencode("media/sprites/ship/shiplife.png")
		self.image = pygame.image.load(os.fsdecode(self.life))
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		self.g_settings = g_settings
		self.rect = self.image.get_rect()

