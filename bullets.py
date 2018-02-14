import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
	
	def __init__(self, screen, g_settings):
		super(Bullet, self).__init__()
		
		self.screen = screen
		
