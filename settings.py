import pygame, os


class Settings():

	# 0 = reg || 1 = twitter
	_current_game = 0
	
	def __init__(self):
		
		self.screen_width = 1200
		self.screen_height = 800
		# Load Image / sprites
		self.fp = os.fsencode("sprites/GameBack1.jpg")
		self.f2 = os.fsencode("sprites/GameBack2.jpg")
		self.background = pygame.image.load(os.fsdecode(self.fp))
		self.background2 = pygame.image.load(os.fsdecode(self.f2))
		# We are only tracking ONE rect during either background
		self.background_rect = self.background.get_rect()
		
		
		# score multiplier
		self.score_mult = 1.25
		self.damage_mult = 1.4
		self.speed_mult = 1.2
		
		# Bullets
		self.bullet_speed = 15
		self.bullet_length = 3
		self.bullet_width = 100
		self.bullet_color = (255,255,190)
		# Lazers
		self.lazer_color = (255,255,190)
		self.lazer_width = 3
		
		# Bombs
		#self.bomb = pygame.image.load("")
		
		# Reticles
		#self.Lazer_ret = 

		# Twitter stuff. Twit = A single letter of a tweet
		self.char_width = 20
		self.char_height = 24
		self.char_spacing = 1
		self.twit_drop_speed = 100
		self.twit_points = 10

		# Create dynamic settings
		self.init_dynamic_settings()
		

	def init_dynamic_settings(self):

		# Twits
		self.twit_direction = 1
		self.twit_speed = 4
		self.twit_hp = 2
		self.score_multiplier = 1.48
		
		# Lives
		self.ship_limit = 1

		# Ship
		self.ship_speed_right = 2.0
		self.ship_speed_up = 3.0
		self.ship_speed_down = 1.8
		self.ship_speed_left = 2.0

		# Aliens (Offline twit mode)
		self.alien_speed = 1
		
		# Damage Grades
		self.bomb_dmg = 2
		self.lazer_dmg = 1
		self.bullet_dmg = 1
		print("DYNAMIC SETTINGS \nLIVES {}".format(self.ship_limit))
		
	# def get_tweet(self):
	# 	""" Called until a game begins """ 
	# 	self.textbox = textbox
	# 	return self.textbox.update(event)



	def change_reticle(self, reticle):
		pass 
		
	def load_background(self, screen, game=0):
		if not game:
			screen.blit(self.background, self.background_rect)
		if game:
			screen.blit(self.background2, self.background_rect)


		
