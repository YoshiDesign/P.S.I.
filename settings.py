import pygame

class Settings():
	
	def __init__(self):
		
		self.screen_width = 1200
		self.screen_height = 800
		self.background = pygame.image.load("media/Back.jpg")
		self.background_rect = self.background.get_rect()
		
		# Lives
		self.ship_limit = 3
		# score multiplier
		self.score_mult = 1.2
		
		# Player Lazer statics
		self.lazer_color = (0, 255, 0)
		self.lazer_width = 1
		
		# Player Bomb statics
		#self.bomb = pygame.image.load("")
		
		# Player Bullet statics
		self.bullet_height = 2
		self.bullet_width = 2
		
		

	def init_dynamic_settings(self):
		
		self.alien_speed = 1
		self.ship_speed_right = 1.2
		self.ship_speed_left = 1.0
		
		# Damage Grades
		self.bomb_dmg = 2
		self.lazer_dmg = 1
		self.bullet_dmg = 1

		
