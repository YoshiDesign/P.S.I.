import pygame
from time import sleep
from pygame.sprite import Sprite

class Bullet(Sprite):
	
	def __init__(self, g_settings, screen, ship, power='', \
										level=0, b_offset=0, \
										mousex=0, mousey=0):
		super(Bullet, self).__init__()
		
	
		self.screen = screen
		self.g_settings = g_settings
		self.power = str(power)
		self.level = int(level)
		self.b_offset = b_offset

		if self.power == 'gun' and self.level > 0:

			self.rect = pygame.Rect(0,0, self.g_settings.gun_width,\
										 	self.g_settings.bullet_length)
			self.rect.centerx 		= ship.rect.centerx
			self.rect.top 			= ship.rect.top
			self.y 					= float(self.rect.y)
			self.color 				= g_settings.bullet_color
			self.speed 				= g_settings.bullet_speed


		# Ima Lazer
		elif self.power == 'lazerup' and self.level > 0:

			self.mousex = mousex
			self.mousey = mousey

			# OPT Rect of a circle?
			self.rect = pygame.Rect(0,0, self.g_settings.lazer_width,\
										 		self.g_settings.lazer_stop)

			if level == 1:
				pass
				

			if level == 2:
				pass
			if level == 3:
				pass
			self.rect.centerx 		= ship.rect.centerx
			self.rect.bottom 		= ship.rect.top
			self.speed 			= 2
			self.x				= float(self.rect.x)
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
			
				self.rect.centerx		= ship.rect.x + (b_offset * 32)
				self.rect.top 			= ship.rect.top + 26
				
			if self.level == 2:
				self.rect.centerx 		= ship.rect.centerx + (b_offset - 2)
				self.rect.top 			= ship.rect.top + 26

			if self.level == 3:
				self.rect.centerx 		= ship.rect.centerx + 3
				self.rect.top 			= ship.rect.top
				
			self.y 				= float(self.rect.y)
			self.x				= float(self.rect.x)
			self.color   		= (255 - (25 * self.level),\
									100 + (50 * self.level),\
									175 + (25 * self.level))
			self.speed = self.g_settings.bullet_speed + (2 * self.level)
			self.g_settings.bullet_dmg 	+= (18 * self.level)

		# Ima friggin' bomb!
		elif self.power == 'bombup' and self.level > 0:


			self.rect = pygame.Rect(0,0, self.g_settings.bullet_width,\
										 self.g_settings.bullet_length)
			self.rect.top = ship.rect.top
			self.rect.centerx = ship.rect.centerx
			if level == 1:
			
				
				pass
				

			if level == 2:
				pass
			if level == 3:
				pass

			self.y = float(self.rect.y)
			self.color = g_settings.bullet_color
			self.speed = g_settings.bullet_speed



	def update(self):
		""" powers[] = Power levels of [bullets, lazer, bomb], oh my """

		# # Tracking weapon levels
		# lazer 		= self.g_settings.lazer
		# bullets 		= self.g_settings.bullets
		# bomb 			= self.g_settings.bomb

		if self.power == 'bulletup' and self.level >= 2:

			self.angle_bullets(self.level)
		
		if self.power == 'lazerup' and self.level > 0:

			self.y -= self.speed
			self.rect.y = self.y

		if self.power == 'bombup' and self.level > 0:

			self.y -= self.speed
			self.rect.y = self.y

		else:
			# Default gun behavior
			self.y -= self.speed
			self.rect.y = self.y
			

	def draw_projectile(self):
		if self.power == 'bulletup':
		
			pygame.draw.rect(self.screen, self.color, self.rect)

		elif self.power == 'lazerup':
			pygame.draw.ellipse(self.screen, self.color, [self.rect.x, self.rect.y, 50, 20])

		elif self.power == 'bombup':
			pass
		else:
			pygame.draw.rect(self.screen, self.color, self.rect)


	def angle_bullets(self, level):

		""" Polymorphic """

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

	def aim_lazer(mousex, mousey):
		pass

	# def power_level(self, level, **kwargs):

	# 	""" 
	# 		If level gets used, use it to diminish returns

	# 		If >9k just += 0 
	# 		0 == bullets
	# 		1 == bombs
	# 		2 == lazer
	# 	"""
	# 	power = "placeholder"
	# 	if self.power == 0:
	# 		self.g_settings.bullet_dmg += (level * 100) # and line extends 1/3 of the way to first pwr marker
			
			
	# 	elif power == 1:
	# 		self.g_settings.bomb_dmg += (level * 100)
			
	# 	elif power == 2:
	# 		self.g_settings.lazer_dmg += (level * 100)
			

	# 	return 0


	# def upgrade_bullets(self):

	# 	pass

	# def upgrade_lazer(self, lazer, init_len):

	# 	pygame.draw.Rect(screen, (205,190,210), [1000, 550, 10, init_len])
	# 	init_len -= 2
	# 	self.screen.flip()
	# 	sleep(0.1)


	# def upgrade_bombs(self):

	# 	pass

	
		
