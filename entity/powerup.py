import os
import pygame
from pygame.sprite import Sprite


class Powerup(Sprite):

	def __init__(self, g_settings, screen, pwr, twit):
		super(Powerup, self).__init__()
		self.g_settings = g_settings
		self.screen = screen

		# type of power up determined by ID assigned to the twit
		self.power = twit.power
		
		self.fp = os.fsencode(str("media/sprites/powers/powerup1a.png"))
		# if pwr == 2:

		# if pwr == 3:

		# if pwr == 4:

		# if pwr == 5:

		self.image = pygame.image.load(os.fsdecode(self.fp))
		self.rect = self.image.get_rect()
		self.rect.top = twit.rect.bottom
		self.rect.centerx = twit.rect.centerx
		self.y = float(self.rect.top)

	def update(self):
		self.y += self.g_settings.pwr_drop_rate
		self.rect.y = self.y

	def blitme(self):
		self.screen.blit(self.image, self.rect)
