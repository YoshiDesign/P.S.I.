import pygame, os


class Settings():

	# 0 = reg || 1 = twitter
	_current_game = 0
	
	def __init__(self):
		
		self.screen_width = 1200
		self.screen_height = 800
		# Load Image / sprites. Keep fsencode / fsdecode plz. 
		# It will help when unicode becomes a thing
		self.f1 = os.fsencode("media/BackMain.jpg")
		self.f2 = os.fsencode("media/BackUsr.jpg")
		self.f3 = os.fsencode("media/BackPwd.jpg")
		self.f4 = os.fsencode("media/GameBack.jpg")
		self.f5 = os.fsencode("media/BackMain2.jpg")
		# self.f5 = os.fsencode("media")

		# SLOW DOWN? If the game slow down, make loading the bg a dynamic init
		# SEPARATE from the dynamic init properties of game elements
		self.background1 = pygame.image.load(os.fsdecode(self.f1))
		self.background2 = pygame.image.load(os.fsdecode(self.f2))
		self.background3 = pygame.image.load(os.fsdecode(self.f3))
		self.background4 = pygame.image.load(os.fsdecode(self.f4))
		self.background5 = pygame.image.load(os.fsdecode(self.f5))

		# We are only tracking ONE rect during any background display
		self.background_rect = self.background1.get_rect()
		
		
		# Static Multipliers
		self.damage_mult = 1.4
		self.speed_mult = 1.15
		
		# Bullets
		self.bullet_speed = 25
		self.bullet_length = 5
		self.bullet_width = 110
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
		self.twit_drop_speed = 65
		self.twit_points = 10

		# Create dynamic settings
		self.init_dynamic_settings()
		
	def init_dynamic_settings(self):
		""" Anything that changes and isnt a power up"""
		# Twits
		self.twit_direction = 1
		self.twit_speed = 4
		self.twit_hp = 2

		# Dynamic multipliers
		self.score_multiplier = 1.00

		# All twits in a tweet have the same id
		self.twit_id = 0
		# Lives
		self.ship_limit = 1
		self.ship_speed = 1

		# Aliens (Offline twit mode)
		self.alien_speed = 1
		
		# Damage Grades
		self.bomb_dmg = 2
		self.lazer_dmg = 1.5
		self.bullet_dmg = 1

		# Pwr-up attribs
		self.pwr_drop_rate = 2

		# Movement Flags
		self.move_right = False
		self.move_left  = False
		self.move_forward = False
		self.turn_left = False
		self.turn_right = False
		self.move_up = False
		self.move_down = False

	

	def change_reticle(self, reticle):
		pass 
		
	def load_background(self, screen, display=0):
		""" 
			display 0 : Main menu
			display 1 : Username
			display 2 : Password
			display 3 : In-Game
			display 4 : Main menu Logged In
			...
		"""
		if not display:
			screen.blit(self.background1, self.background_rect)
		elif display == 1:
			screen.blit(self.background2, self.background_rect)
		elif display == 2:
			screen.blit(self.background3, self.background_rect)
		elif display == 3:
			screen.blit(self.background4, self.background_rect)
		elif display == 4:
			screen.blit(self.background5, self.background_rect)






		
