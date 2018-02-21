import pygame
import os
from tools.spritesheet import Spritesheet

class Explosion():

	def __init__(self, g_settings, screen, twit):
		self.screen = screen
		self.twit = twit
		self.fp = os.fsencode("spritesheets/splodesheet.png")
		self.sheet = Spritesheet(self.fp, 5, 4, index=0)
		self.loc_x = self.twit.rect.centerx
		self.loc_y = self.twit.rect.centery

	def explode(self, loop=20):
		for index in range(loop):
			self.sheet.blitme(self.screen, index % self.sheet.totalCells, \
														self.loc_x, self.loc_y)
