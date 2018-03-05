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

		# type of power up determined by twit.power
		self.pwr = pwr

		# used to rotate sprite
		self.x = randint(1,3)

		if g_settings.is_Trump: # FURTEHR CONDSIDERATION -- if we land on lazer, bullet or bomb, roll 0,2. if 2, spawn it, if not, score mult, speed or freeze

			self.fp = os.fsencode(str("media/sprites/powers/mflag.png"))
		elif self.pwr == 1:
			self.fp = os.fsencode(str("media/sprites/powers/bulletup.png"))
		elif self.pwr == 2:
			self.fp = os.fsencode(str("media/sprites/powers/bombup.png"))
		elif self.pwr == 3:
			self.fp = os.fsencode(str("media/sprites/powers/lazerup.png"))
		elif self.pwr == 4:
			self.fp = os.fsencode(str("media/sprites/powers/freezeup.png"))
		elif self.pwr == 5:
			self.fp = os.fsencode(str("media/sprites/powers/speedup.png"))
		else:
			self.fp = os.fsencode(str("media/sprites/powers/scoreup.png"))

		self.image = pygame.image.load(os.fsdecode(self.fp))
		self.rect = self.image.get_rect()
		# Falls from :
		self.rect.top = twit_rect.bottom
		self.rect.centerx = twit_rect.centerx
		# Movement
		self.y = float(self.rect.top)

	def update(self):
		# Movement
		self.y += self.g_settings.pwr_drop_rate
		self.rect.y = self.y

	def blitme(self):
		self.screen.blit(self.image, self.rect)
