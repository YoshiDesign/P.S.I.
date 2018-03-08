import pygame, os


class Settings():

	# 0 = reg || 1 = twitter
	_current_game = 0
	
	def __init__(self):
		
		self.screen_width 	= 1200
		self.screen_height 	= 800

		# Load Image / sprites. 
		self.f1 = os.fsencode("media/BackMain.jpg")
		self.f2 = os.fsencode("media/BackUsr.jpg")
		self.f3 = os.fsencode("media/BackPwd.jpg")
		self.f4 = os.fsencode("media/GameBack.jpg")
		self.f5 = os.fsencode("media/BackMain2.jpg")
		# self.f5 = os.fsencode("media")

		# If the game slows down, make loading the bg a dynamic init,
		# SEPARATE from the dynamic init properties of game elements. Make sure it only happens once
		self.background1 = pygame.image.load(os.fsdecode(self.f1))
		self.background2 = pygame.image.load(os.fsdecode(self.f2))
		self.background3 = pygame.image.load(os.fsdecode(self.f3))
		self.background4 = pygame.image.load(os.fsdecode(self.f4))
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
		self.gun_width 		= 110

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

		self.is_Trump = False

		# Create dynamic settings
		self.init_dynamic_settings()

		
	def init_dynamic_settings(self):
		""" Anything that changes and isnt a power up"""
		
		# Twits
		self.twit_direction = 1
		# Change in x
		self.twit_speed 	= 4
		# Change in y
		self.twit_drops 	= 40
		self.twit_hp 		= 200
		# Twit uid
		self.twit_id 		= 0

		# Dynamic multipliers
		self.score_multi 	= 1.00

		# Lives
		self.ship_limit 	= 1
		self.ship_speedup 	= 1.2

		# Damage Grades
		self.bomb_dmg 		= 200
		self.lazer_dmg 		= 50
		self.bullet_dmg 	= 100

		# Ammo
		self.lazer_ammo = 0
		self.bullets_ammo = 0
		self.bomb_ammo = 0

		# Pwr-up attribs
		self.pwr_drop_rate 	= 2

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

		# weapons for upgrading
		self.lazer 		= 0
		self.bullets 	= 0
		self.bomb 		= 0

		

	def reset_weapon_damage(self, weapon):

		if weapon == 1:
			# bullets
			self.bullet_dmg = 100
		if weapon == 2:
			# lazer
			self.lazer_dmg = 50
		if weapon == 3:
			# bomb
			self.bom_dmg = 200

	# Special opponents
	def reset_special(self):
		self.is_Trump = False
		self.is_Yoshi = False

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
			screen.blit(self.background4, self.background_rect)
		elif display == 4:
			screen.blit(self.background5, self.background_rect)






		
