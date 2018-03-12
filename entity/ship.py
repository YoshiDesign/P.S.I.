
import pygame
from pygame.sprite import Sprite
import sys, os
from tools.spritesheet import Spritesheet

class Ship(Sprite):

	# 0 = reg || 1 = twitter
	

	def __init__(self, screen, g_settings, stats, no_sprite=0):

		super(Ship, self).__init__()

		self.g_settings = g_settings
		# Get screen & Screen Object
		self.screen = screen
		self.stats = stats
		self.screen_rect = screen.get_rect()

		self.fp = os.fsencode("media/spritesheets/shipsheet.png")
		self.sheet = Spritesheet(self.fp, 4, 1)
		# Used for life counter
		self.index = 0
		
		# Since we blit the boat based on a spritesheet, we need initial static allocation to start
		# Note : The ship image follows a manually instantiated pygame.Rect its rect, not vice versa
		self.ship_x = 600
		self.ship_y = 700
		self.rect = pygame.Rect(self.ship_x, self.ship_y, 32, 32)

		# Tighten the collision model

		self.ship_speed_right 	= 5.0
		self.ship_speed_up 		= 3.0
		self.ship_speed_down 	= 2.0
		self.ship_speed_left 	= 5.0

		self.rect.inflate(-4, -4)
		
		self.power_up()

	def update(self):

		if self.index < 100:
			self.index += 1
		else:
			self.index = 0

		# Blit the ship on the screen, iterating through its spritesheet indices
		self.sheet.blitme(self.screen, self.index % self.sheet.totalCells, \
												self.ship_x, self.ship_y)
		
		# Movement Sensors
		if self.g_settings.move_right and self.ship_x < self.screen_rect.right + 40:
			self.ship_x += self.ship_speed_right

		if self.g_settings.move_left and self.ship_x > self.screen_rect.left - 40:
			self.ship_x -= self.ship_speed_left

		# Twiter Mode upper allowance
		if self.g_settings.move_up and self.ship_y > self.screen_rect.centery + 250 \
					and self.stats._current_screen == 3:
			self.ship_y -= self.ship_speed_up

		# Reg Mode upper allowance
		elif self.g_settings.move_up and self.ship_y > self.screen_rect.top \
					and not self.stats._current_screen == 5:
			self.ship_y -= self.ship_speed_up

		if self.g_settings.move_down and self.ship_y < self.screen_rect.bottom:
			self.ship_y += self.ship_speed_left

		# Strafe
		if self.g_settings.strafe_L and self.ship_y > self.screen_rect.top and \
			self.ship_x > self.screen_rect.left:
			
			self.g_settings.strafe_L = False

		if self.g_settings.strafe_R and self.ship_y > self.screen_rect.top and \
			self.ship_x < self.screen_rect.right:
			
			self.g_settings.strafe_R = False

		self.rect.x = self.ship_x
		self.rect.y = self.ship_y
			
	def center_ship(self):
		self.ship_x = self.screen_rect.centerx
		self.ship_y = 700

		# self.center = self.screen_rect.centerx


	def power_up(self, pwr=''):
		""" 
			Must be called to fully initialize the ship
			when pwr=False, g_settings.(pwr) is 3/3
		"""

		if pwr == False:
			""" Already max upgrade """
			return 0

		# OPT could use map, but values differ...moot
		pwr = pwr.lower()

		if pwr == 'speedup': 
			# Game is Starting or we picked up a speed powerup
			self.ship_speed_right 	*= self.g_settings.ship_speedup
			self.ship_speed_up 		*= self.g_settings.ship_speedup
			self.ship_speed_down 	*= self.g_settings.ship_speedup
			self.ship_speed_left 	*= self.g_settings.ship_speedup

		return True

		
