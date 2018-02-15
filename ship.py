import pygame
import sys, os
from spritesheet import Spritesheet

class Ship():

	# 0 = reg || 1 = twitter
	_current_game = 0

	def __init__(self, screen, g_settings, stats):
		
		self.fp = os.fsencode("spritesheets/shipsheet.png")
				
		# Get screen & Screen Object
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.stats = stats
		self.sheet = Spritesheet(self.fp, 4, 1)
		self.index = 0
		self.settings = g_settings
		
		# Ship Positioning
		#~ self.rect.centerx = self.screen_rect.centerx
		#~ self.rect.bottom = self.screen_rect.bottom + 10
		
		self.ship_x = 600
		self.ship_y = 700
		
		# Movement Flags
		self.move_right = False
		self.move_left  = False
		self.move_forward = False
		self.turn_left = False
		self.turn_right = False
		self.move_up = False
		self.move_down = False

	@staticmethod
	def switch_game():
		Ship._current_game = 1

	def update(self):
		
		if self.index < 100:
			self.index += 1
		else:
			self.index = 0
		
		# Blit the ship on the screen, iterating through its spritesheet indices
		self.sheet.blitme(self.screen, self.index % self.sheet.totalCells, \
												self.ship_x, self.ship_y)
		
		# Movement Sensors
		if self.move_right and self.ship_x < self.screen_rect.right:
			self.ship_x += self.settings.ship_speed_right
		if self.move_left and self.ship_x > self.screen_rect.left:
			self.ship_x -= self.settings.ship_speed_left
		# Twiter Mode upper allowance
		if self.move_up and self.ship_y > self.screen_rect.centery - 250 \
					and self.stats._current_game:
			self.ship_y -= self.settings.ship_speed_up
		# Reg Mode upper allowance
		elif self.move_up and self.ship_y > self.screen_rect.top \
					and not self.stats._current_game:
			self.ship_y -= self.settings.ship_speed_up
		if self.move_down and self.ship_y < self.screen_rect.bottom:
			self.ship_y += self.settings.ship_speed_left
	
	

			
			
			
			
			
			
		
		
			
			
		
	def center_ship(self):
		self.center = self.screen_rect.centerx
	
		
		
		
