import os
import pygame
from pygame.sprite import Sprite


class Powerup(Sprite):

	def __init__(self, g_settings):
		super(Powerup, self).__init__()
		self.g_settings = g_settings
		
	