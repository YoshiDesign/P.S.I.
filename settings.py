import pygame, os
from analyze import Analyzer

class Settings():

	# 1 = Twitter mode (only one flag currently in use)
	_current_game = 0
	
	def __init__(self, exit):

		""" All basic game settings """
		
		self.screen_width 	= 1200
		self.screen_height 	= 800

		# Load Image / sprites. 
		self.f1 = os.fsencode("media/BackMain.jpg")
		self.f2 = os.fsencode("media/BackUsr.jpg")
		self.f3 = os.fsencode("media/BackPwd.jpg")
		self.f4 = os.fsencode("media/GameBack.jpg")
		self.f5 = os.fsencode("media/BackMain2.jpg")
		self.fY = os.fsencode("media/GameBackY.jpg")
		# self.f5 = os.fsencode("media")

		# If the game slows down, make loading the bg a dynamic init,
		# SEPARATE from the dynamic init properties of game elements. Make sure it only happens once
		self.background1 = pygame.image.load(os.fsdecode(self.f1))
		self.background2 = pygame.image.load(os.fsdecode(self.f2))
		self.background3 = pygame.image.load(os.fsdecode(self.f3))
		self.background4 = pygame.image.load(os.fsdecode(self.f4))
		self.backgroundY = pygame.image.load(os.fsdecode(self.fY))
		self.background5 = pygame.image.load(os.fsdecode(self.f5))

		# Any of the bg's will do for tracking
		self.background_rect = self.background1.get_rect()
		
		# Static Multipliers
		self.damage_mult 	= 1.4
		self.speed_mult 	= 1.15
		
		# Bullets
		self.bullet_speed 	= 25
		self.bullet_length 	= 2
		self.bullet_width 	= 1
		self.bullet_color 	= (255,255,190)
		self.gun_width 		= 3

		# Lazers
		self.lazer_color 	= (255, 0, 0)
		self.lazer_width 	= 100
		self.lazer_stop 	= 20 

		# Bomb
		self.bomb_color 	= (255, 190, 0)
		
		# Word stuff. Twit = A single letter of a tweet
		self.char_width 	= 20
		self.char_height 	= 24
		self.char_spacing 	= 1

		# Static points
		self.twit_points 	= 10

		# Required in Init for stats.reset
		self.ship_limit = 3

		# Create dynamic settings
		self.init_dynamic_settings()

		
	def init_dynamic_settings(self, difficulty=0):
		""" Anything that changes and isnt a power up"""

		self.diff = int(difficulty)
		if self.diff > 30:
			# Lives
			self.ship_limit 	= 1
		
		self.twit_hp = 200
		# Y
		self.twit_drops 	= 40
		# X
		self.twit_speed		= 4
			
	
		# Pwr-up attribs
		self.pwr_fall_rate	= 2
		# <- or +>
		self.twit_direction = 1
		# Twit uid
		self.twit_id 		= 0
		# Dynamic multipliers
		self.score_multi 	= 1.00
		self.ship_speedup 	= 1.2

		# Movement Flags
		self.move_right 	= False
		self.move_left  	= False
		self.move_forward 	= False
		self.strafe_L 		= False
		self.strafe_R	 	= False
		self.move_up 		= False
		self.move_down 		= False
		# Shooting flag
		self.firing 		= False

		# Weapon Levels
		self.lazer 		= 0
		self.bullets 	= 0
		self.bomb 		= 0
		self.default_gun = 1
		# Ammos
		self.lazer_ammo = 0
		self.bullets_ammo = 0
		self.bomb_ammo 	= 0
		# Damages
		self.bullet_dmg = 200
		self.lazer_dmg 	= 10
		self.bomb_dmg 	= 5
		
	def reset_weapon_damage(self, weapon):

		if weapon == 1:
			self.bullet_dmg = 90
		if weapon == 2:
			self.lazer_dmg = 10
		if weapon == 3:
			self.bomb_dmg = 5

	# Special opponents
	def set_special(self):
		self.is_Trump = False
		self.is_Yoshi = False
		self.is_ElonX = False

	def clear_weapon(self, power):
		if power == "lazerup":
			self.lazer = 0
		elif power == "bombup":
			self.bomb = 0
		elif power == "bulletup":
			self.bullets = 0
		
	def load_background(self, screen, display=0):
		""" 
			display 0 : Main menu
			display 1 : Username
			display 2 : Password
			display 3 : In-Game
			display 4 : Main menu Logged In
			
		"""
		if not display:
			screen.blit(self.background1, self.background_rect)
		elif display == 1:
			screen.blit(self.background2, self.background_rect)
		elif display == 2:
			screen.blit(self.background3, self.background_rect)
		elif display == 3:
			if self.is_Yoshi:
				screen.blit(self.backgroundY, self.background_rect)
			else:
				screen.blit(self.background4, self.background_rect)
		elif display == 4:
			screen.blit(self.background5, self.background_rect)


