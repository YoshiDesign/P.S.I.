import pygame
import os
from tools.spritesheet import Spritesheet

class Explosion():

	def __init__(self, g_settings, screen, twit):
		self.screen = screen
		self.twit = twit
		self.fp = os.fsencode("media/spritesheets/splodesheet.png")
		self.sheet = Spritesheet(self.fp, 5, 4)
		self.loc_x = self.twit.rect.centerx
		self.loc_y = self.twit.rect.centery

	def explode(self, i=16):
		for index in range(i):
			self.sheet.blitme(self.screen, index % self.sheet.totalCells, \
														self.loc_x, self.loc_y)
