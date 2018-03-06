import pygame
from time import sleep
from pygame.sprite import Sprite
from multiprocessing import Process, Queue

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

		# Max length of upgrade viz lines
		self.init_len = 100

	def power_level(self, level, **kwargs):

		""" 
			If level gets used, use it to diminish returns

			If >9k just += 0 
			0 == bullets
			1 == bombs
			2 == lazer
		"""
		power = "placeholder"
		if power == 0:
			self.g_settings.bullet_dmg += (level * 100) # and line extends 1/3 of the way to first pwr marker
			
			
		elif power == 1:
			self.g_settings.bomb_dmg += (level * 100)
			
		elif power == 2:
			self.g_settings.lazer_dmg += (level * 100)
			

		return 0


	def upgrade_bullets(self):

		pass

	def upgrade_lazer(self, lazer, init_len):

		pygame.draw.Rect(screen, (255,255,255), [1000, 550, 10, init_len])
		init_len -= 2
		self.screen.flip()
		sleep(0.1)


	def upgrade_bombs(self):

		pass

	def update(self):
		# Linear movement
		self.y -= self.speed
		self.rect.y 	= self.y

		# Tracking weapon levels : Each can be 0 -> 3
		self.lazer 		= self.g_settings.lazer
		self.bullets 	= self.g_settings.bullets
		self.bomb 		= self.g_settings.bomb

		if self.lazer:
			
			# LQ = Queue()
			# LQ.put(self.lazer)

			# L = Process(target=self.upgrade_lazer, args=(LQ, self.init_len))

			# L.start()

			# self.g_settings.lazer -= 1
			pass

		if self.g_settings.bullets:
			pass
		if self.g_settings.bomb:
			pass
				

			

		

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)

		
