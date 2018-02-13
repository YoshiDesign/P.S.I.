import pygame
import sys, os
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, screen, g_settings):
		super(Ship, self).__init__()
		self.screen = screen
		self.settings = g_settings
		
		self.animate = []
		
	def load_image(self, name):
		""" Acquire sprite from FS """
		path_to_sprite = os.path("sprites/" + name)
		image = pygame.image.load(path_to_sprite)
		return image
		

	def update(self):
		pass
		
		
		
		
