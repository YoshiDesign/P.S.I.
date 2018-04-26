import os
import pygame
from random import randint
from pygame.sprite import Sprite


class Powerup(Sprite):

	""" 
		Create a power up 
		Determined by twit.power (pwr)
	"""
	def __init__(self, g_settings, screen, pwr, twit_rect):

		super(Powerup, self).__init__()
		self.g_settings = g_settings
		self.screen = screen

		# all pwr ups are worth 20 pts
		self.point = 20

		# type of power up
		self.pwr = pwr

		# used to rotate sprite
		self.x = randint(1,4)
		if self.g_settings.is_Trump:
			if self.x == 1:
				self.fp = os.fsencode(str("media/sprites/powers/specials/mflag.png"))
			else:
				self.fp = os.fsencode(str("media/sprites/powers/specials/money.png"))

		elif self.g_settings.is_Yoshi:
			if self.x == 1:
				self.fp = os.fsencode(str("media/sprites/powers/specials/mariobro.png"))
			if self.x == 2:
				self.fp = os.fsencode(str("media/sprites/powers/specials/snowman.png"))
			if self.x == 3: 
				self.fp = os.fsencode(str("media/sprites/powers/specials/spellbook.png"))
			if self.x == 4: 
				self.fp = os.fsencode(str("media/sprites/powers/specials/redfeather.png"))
		elif self.g_settings.is_ElonX:
			pass
		else:
			self.fp = os.fsencode(str('media/sprites/powers/') + str(pwr) + str('.png'))

		self.image = pygame.image.load(os.fsdecode(self.fp)).convert_alpha()
		self.rect = self.image.get_rect()
		# Falls from :
		self.rect.top = twit_rect.bottom
		self.rect.centerx = twit_rect.centerx
		# Movement
		self.y = float(self.rect.top)

	def update(self):
		# Movement
		self.y += self.g_settings.pwr_fall_rate
		self.rect.y = self.y

	def blitme(self):
		self.screen.blit(self.image, self.rect)
