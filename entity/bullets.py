import os
import pygame
from math import sin, cos, pi
from time import sleep, time
from pygame.sprite import Sprite
from tools.spritesheet import Spritesheet

class Bullet(Sprite):
	
	def __init__(self, g_settings, screen, ship, power='', \
										level=0, b_offset=0):
		super(Bullet, self).__init__()
		
		self.screen = screen
		self.ship = ship
		self.g_settings = g_settings

		# Constant for keeping relative to the ship
		self.position_x = ship.ship_x - 400
		# Relative speed constant
		self.speed = float(3.0)

		# Increment spritesheets
		self.step 	= 0
		self.index 	= 0

		# For Lazer vector
		self.delta_x = 0
		self.delta_y = 0

		# Properties
		self.power = str(power)
		self.level = int(level)

		# Bullet vector constant
		self.b_offset = b_offset

		if self.power == 'gun' and self.level > 0:

			self.rect = pygame.Rect(0,0, self.g_settings.gun_width,\
									self.g_settings.bullet_length)

			self.rect.centerx 		= self.ship.rect.centerx
			self.rect.top 			= self.ship.rect.top
			self.y 					= float(self.rect.y)
			self.color 				= g_settings.bullet_color
			self.speed 				= g_settings.bullet_speed

		# Ima Lazer
		elif self.power == 'lazerup' and self.level > 0:
			
			# AIM
			self.mousex, self.mousey = pygame.mouse.get_pos()
			
			self.frequency = 3
			self.amplitude = 20

			if level == 1:
				self.fp = os.fsencode("media/spritesheets/splodesheet.png")
			elif level == 2:
				self.fp = os.fsencode("media/spritesheets/splodesheetL2.png")
			elif level == 3:
				self.fp = os.fsencode("media/spritesheets/splodesheetL3.png")
			else:
				self.fp = os.fsencode("media/spritesheets/splodesheet.png")

			self.sheet = Spritesheet(self.fp, 5, 4)
			self.rect = pygame.Rect(0,0, 32, 32)
			self.rect.x = self.ship.rect.x
			self.rect.y = self.ship.rect.y

			self.speed 			= 2
			self.x				= float(self.ship.ship_x)
			self.y			 	= float(self.rect.y)

			# self.color   		= (175 + (25 * self.level), 0, 175 + (25 * self.level))
			self.g_settings.lazer_dmg += (4 * self.level)



			self.delta_y = float(self.ship.rect.y - self.mousey) * -1
			self.delta_x = float(self.x - self.mousex)

			self.zero_y = self.mousey - self.mousey

			self.slope = float(self.delta_y / self.delta_x)

			# print("SLOPE = {}".format(self.slope))

		# Ima Bullet
		elif self.power == 'bulletup' and self.level > 0:

			self.rect 			= pygame.Rect(0,0, self.g_settings.bullet_width,\
										 	 	self.g_settings.bullet_length * 5)
			
			if self.level == 1:
			
				self.rect.centerx		= self.ship.rect.x + (b_offset * 32)
				self.rect.top 			= self.ship.rect.top + 26
				
			if self.level == 2:
				self.rect.centerx 		= self.ship.rect.centerx + (b_offset - 2)
				self.rect.top 			= self.ship.rect.top + 26

			if self.level == 3:
				self.rect.centerx 		= self.ship.rect.centerx + 3
				self.rect.top 			= self.ship.rect.top
				
			self.y 				= float(self.rect.y)
			self.x				= float(self.rect.x)
			self.color   		= (255 - (25 * self.level),\
									100 + (50 * self.level),\
									175 + (25 * self.level))
			self.speed = self.g_settings.bullet_speed + (2 * self.level)
			self.g_settings.bullet_dmg 	+= (18 * self.level)

		# Ima Bomb
		elif self.power == 'bombup' and self.level > 0:

			self.frequency = 1
			self.amplitude = 40
			self.offset_value = self.b_offset * 32

			if level == 1:

				if self.g_settings.is_Yoshi:
					self.fp = os.fsencode("media/sprites/powers/specials/yoshieg.png")
				else:
					self.fp = os.fsencode("media/sprites/powers/fireball.png")
					
			if level == 2:

				if self.g_settings.is_Yoshi:
					self.fp = os.fsencode("media/sprites/powers/specials/yoshieg.png")
				else:
					self.fp = os.fsencode("media/sprites/powers/fireball2.png")

			if level == 3:

				if self.g_settings.is_Yoshi:
					self.fp = os.fsencode("media/sprites/powers/specials/yoshieg.png")
				else:
					self.fp = os.fsencode("media/sprites/powers/fireball3.png")

			self.image	 	= pygame.image.load(os.fsdecode(self.fp))
			self.rect 		= self.image.get_rect()
			self.rect.top 	= self.ship.rect.top
			self.rect.centerx 	= self.ship.rect.x + self.offset_value
			self.y 				= float(self.rect.y)
			self.speed 			= self.speed + 8
			self.g_settings.bomb_dmg += (3 * self.level)

	def update(self, *args):

		""" Incremental changes in location """

		# Update Bullets
		if self.power == 'bulletup' and self.level >= 2:
			self.angle_bullets(self.level)
		
		# Update Lazer
		if self.power == 'lazerup' and self.level > 0:

			self.index += 1
			if self.index % 12:
				self.step += 1
			
			self.y -= self.speed


			self.rect.y = self.y
			self.rect.x = self.x

			# print("SLOPE??? ", self.slope)
			self.sheet.blitme(self.screen, self.step % self.sheet.totalCells, \
														self.rect.x, self.rect.y)

		# Update Bombs
		if self.power == 'bombup' and self.level > 0:
			self.bomb_vector()

		# Update Default
		else:
			self.y -= self.speed
			self.rect.y = self.y

		pygame.display.flip()



	def draw_projectile(self):
		"""  Cannons  """
		if self.power == 'bulletup' or self.power == 'gun':
		
			pygame.draw.rect(self.screen, self.color, self.rect)
			
		return 0

	def angle_bullets(self, level):

		""" 
			Fan out the bullets based upon a constant.
			Is polymorphic
		"""
		total_levels = float((level * 2) + 1)
		level = float(level)

		for i in range(1, int(total_levels)):
				
				if self.b_offset + 1 == i:
					# left side
					if total_levels / i >= (total_levels / level):

						self.x -= 2 * (total_levels - (i * 2))
						
					# Right side
					else:
						self.x += 2 * (total_levels - ((i-2) * 2))

					self.rect.centerx = self.x

	def bomb_vector(self):

		""" Messy Maths, attempting to organize """

		if self.b_offset == 0:
			op = sin
		else:
			op = cos

		self.y -= self.speed
		self.rect.y = self.y
		# MMMMMMMMMMMMMMMMMMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATHS
		self.x = int((self.g_settings.screen_height/2) + self.amplitude*op(self.frequency*((float(self.y)/self.g_settings.screen_width)*(2*pi) + (self.speed*time()))))
		if self.b_offset == 0:
			self.rect.x = self.x + self.position_x - 16
		elif self.b_offset == 1:
			self.rect.x = self.x + self.position_x + 16
		self.screen.blit(self.image, self.rect)


		