import os
import pygame
from math import sin, cos, pi
from time import sleep, time
from pygame.sprite import Sprite
from tools.spritesheet import Spritesheet

class Bullet(Sprite):
	
	def __init__(self, g_settings, screen, ship, power='', \
												level=0, b_offset=0, \
												mousex=0, mousey=0):
		super(Bullet, self).__init__()
		
		# Otherwise we are stuck relative to the ship's X at instantiation
		self.position_x = ship.ship_x - 400
		self.speed = float(3.0)
		self.step = 0
		self.index = 0
		self.screen = screen
		self.ship = ship
		self.g_settings = g_settings
		# Properties
		self.power = str(power)
		self.level = int(level)
		# Used to angle bullet upgrade - specifically
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
			
			self.mousex = mousex
			self.mousey = mousey
			

			self.frequency = 3
			self.amplitude = 20

			# OPT Rect of a circle?
			self.fp = os.fsencode("media/spritesheets/splodesheet.png")
			self.sheet = Spritesheet(self.fp, 5, 4)
			self.rect = pygame.Rect(0,0, 32, 32)
			self.rect.x = self.ship.rect.x
			self.rect.y = self.ship.rect.y
			
			if level == 1:
				pass
			if level == 2:
				pass
			if level == 3:
				pass

			self.speed 			= 2
			self.x				= float(self.ship.rect.x)
			self.y			 	= float(self.rect.y)
			self.color   		= (175 + (25 * self.level),\
									0,\
									175 + (25 * self.level))
			self.g_settings.lazer_dmg += (5 * self.level)

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

	def update(self, *args):
		""" powers[] = Power levels of [bullets, lazer, bomb], oh my """

		# # Tracking weapon levels
		# lazer 		= self.g_settings.lazer
		# bullets 		= self.g_settings.bullets
		# bomb 			= self.g_settings.bomb

		# Update Bullets
		if self.power == 'bulletup' and self.level >= 2:
			self.angle_bullets(self.level)
		
		# Update Lazer
		if self.power == 'lazerup' and self.level > 0:
			self.index += 1
			if self.index % 12:
				self.step += 1
			self.bomb_lazer(lazer=True, step=self.step)
			
		# Update Bombs
		if self.power == 'bombup' and self.level > 0:
			self.bomb_lazer(bomb=True)

		# Update Default
		else:
			self.y -= self.speed
			self.rect.y = self.y

	def draw_projectile(self):

		if self.power == 'bulletup' or self.power == 'gun':
		
			pygame.draw.rect(self.screen, self.color, self.rect)
			
		return 0

	def angle_bullets(self, level):

		""" Creates constant (level) based angles """

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


	def aim_lazer(self, mousex, mousey):
		pass


	def bomb_lazer(self, bomb=False, lazer=False, step=0):

		""" Messy Maths, attempting to organize """

		if self.b_offset == 0:
			op = sin
		else:
			op = cos

		self.x = int((self.g_settings.screen_height/2) + self.amplitude*op(self.frequency*((float(self.y)/self.g_settings.screen_width)*(2*pi) + (self.speed*time()))))
		self.y-= self.speed
		self.rect.y=self.y

		if bomb:
			if self.b_offset == 0:
				self.rect.x = self.x + self.position_x - 16
			elif self.b_offset == 1:
				self.rect.x = self.x + self.position_x + 16
			self.screen.blit(self.image, self.rect)


		if lazer:
			step = step
			self.sheet.blitme(self.screen, step % self.sheet.totalCells, \
													self.rect.x, self.rect.y)

		pygame.display.flip()

		