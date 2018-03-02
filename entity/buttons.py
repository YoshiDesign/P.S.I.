import pygame.font

class Button():

	# 0 = reg || 1 = twitter
	
	def __init__(self, g_settings, screen, points, color=(0,255,200)):
		
		self.g_settings = g_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.points = points

		self.color = color
		self.color2 = (0,255,255)
		
		self.rect = pygame.draw.rect(screen, self.color, \
					[self.points[0], self.points[1], \
					self.points[2], self.points[3] ],2)


		# Required
	# 	self.prep_msg(text)

	# def prep_msg(self, msg):
	# 	""" Might not need this method """
	# 	self.msg_image = self.font.render(self.text, True, self.text_color)
	# 	self.msg_rect = self.msg_image.get_rect()
	# 	self.msg_rect.center = self.rect.center

	def create_button(self, hover=0):
		""" Button Factory """
		# self.screen.blit(self.screen, self.rect)
		pygame.draw.rect(self.screen, self.color2, \
					[self.points[0], self.points[1], \
					self.points[2], self.points[3] ],2)


# OPTIMIZATIONS : create buttons in a dict
				# redux on how they are created/drawn