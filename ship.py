import pygame
import sys, os
from spritesheet import Spritesheet

class Ship():
	
	def __init__(self, screen, g_settings):
		
		self.fp = os.fsencode("spritesheets/shipsheet.png")
				
		# Get screen & Screen Object
		self.screen = screen
		self.screen_rect = screen.get_rect()
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


	def update(self):
		
		if self.index < 100:
			self.index += 1
		else:
			self.index = 0
		
		# Blit the ship on the screen, iterating through its spritesheet indices
		self.sheet.blitme(self.screen, self.index % self.sheet.totalCells, self.ship_x, self.ship_y)
		
		# Movement Sensor
		if self.move_right and self.ship_x < self.screen_rect.right:
			self.ship_x += self.settings.ship_speed_right
		if self.move_left and self.ship_x > self.screen_rect.left:
			self.ship_x -= self.settings.ship_speed_left
		if self.move_up and self.ship_y > self.screen_rect.centery:
			# Uses same speed for UP as it does for RIGHT
			self.ship_y -= self.settings.ship_speed_up
		if self.move_down and self.ship_y < self.screen_rect.bottom:
			# Enumeration == mootsauce
			self.ship_y += self.settings.ship_speed_left
			
			
			
			
			
			
		
		
			
			
		
	def center_ship(self):
		self.center = self.screen_rect.centerx
	
		
		
		
