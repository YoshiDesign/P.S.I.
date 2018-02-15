import pygame, os

class Settings():

	# 0 = reg || 1 = twitter
	_current_game = 0
	
	def __init__(self):
		
		self.screen_width = 1200
		self.screen_height = 800
		# Load Image / sprites
		self.fp = os.fsencode("media/Back.jpg")
		self.background = pygame.image.load(os.fsdecode(self.fp))
		self.background_rect = self.background.get_rect()
		
		# Lives
		self.ship_limit = 3
		# score multiplier
		self.score_mult = 1.2
		
		# Lazer
		self.lazer_color = (0, 255, 0)
		self.lazer_width = 1
		
		# Da Bomb
		#self.bomb = pygame.image.load("")
		
		# Player Bullet statics
		self.bullet_height = 2
		self.bullet_width = 2
		
		# Reticles
		#self.Lazer_ret = 


		@staticmethod
		def switch_game():
			Settings._current_game = 1
		
		#
		self.init_dynamic_settings()

	def init_dynamic_settings(self):
		
		self.alien_speed = 1
		self.ship_speed_right = 1.8
		self.ship_speed_up = 3.0
		self.ship_speed_down = 1.8
		self.ship_speed_left = 1.8
		
		# Damage Grades
		self.bomb_dmg = 2
		self.lazer_dmg = 1
		self.bullet_dmg = 1
		
	# def get_tweet(self):
	# 	""" Called until a game begins """ 
	# 	self.textbox = textbox
	# 	return self.textbox.update(event)



	def change_reticle(self, reticle):
		
		pass 
		
	def load_background(self, screen):

		screen.blit(self.background, self.background_rect)

		#self.reticle.blit(self.background)


		
