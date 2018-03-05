import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	
	def __init__(self, g_settings, screen, ship, powers={}):
		super(Bullet, self).__init__()
		
		self.screen = screen
		self.g_settings = g_settings
		self.rect = pygame.Rect(0,0, self.g_settings.bullet_width,\
									 self.g_settings.bullet_length)

		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		self.y = float(self.rect.y)

		self.color = g_settings.bullet_color
		self.speed = g_settings.bullet_speed

	def power_level(self, power, level=1):

		""" 
			If level gets used, use it to diminish returns

			If >9k just += 0 
			0 == bullets
			1 == bombs
			2 == lazer
		"""
		if power == 0:
			self.g_settings.bullet_dmg += (level * 100) # and line extends 1/3 of the way to first pwr marker
			self.check_bullets()
			return 0
		elif power == 1:
			self.g_settings.bomb_dmg += (level * 100)
			self.check_lazer()
		elif power == 2:
			self.g_settings.lazer_dmg += (level * 100)
			self.check_bombs()



	def check_bullets(self):

		pass

	def check_lazer(self):

		pass

	def check_bombs(self):

		pass

	def update(self):

		self.y -= self.speed
		self.rect.y = self.y

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)

		
