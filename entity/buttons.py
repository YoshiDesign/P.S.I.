import pygame.font

class Button():

	# 0 = reg || 1 = twitter
	
	def __init__(self, g_settings, screen, p1, p2, p3, p4, color=(0,255,200)):
		
		self.g_settings = g_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4

		self.color = color
		self.color2 = (255,255,255)
		
		self.rect = pygame.draw.rect(screen, self.color, \
					[self.p1, self.p2, self.p3, self.p4 ],2)


		# Required
	# 	self.prep_msg(text)

	# def prep_msg(self, msg):
	# 	""" Might not need this method """
	# 	self.msg_image = self.font.render(self.text, True, self.text_color)
	# 	self.msg_rect = self.msg_image.get_rect()
	# 	self.msg_rect.center = self.rect.center

	def create_button(self, hover=0):
		""" Button Factory """
		self.screen.blit(self.screen_rect, self.rect)


# OPTIMIZATIONS : create buttons in a dict
				# redux on how they are created/drawn