import pygame.font

class Button():

	# 0 = reg || 1 = twitter
	_current_game = 0
	
	def __init__(self, g_settings, screen, \
						text="", width=200, \
				 		height=50, color=(0,255,200), \
				 		text_color=(0,0,0), \
				 		font_size=32, \
				 		off_x=0, off_y=0):
		
		self.g_settings = g_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		self.text = text
		# Dimensions / properties
		self.width, self.height = (width, height)
		self.color = color
		self.text_color = text_color
		self.font = pygame.font.SysFont(None, font_size)
		# Form
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.centerx = self.screen_rect.centerx + off_x
		self.rect.centery = self.screen_rect.centery + off_y

		# Required
		self.prep_msg(text)


	def prep_msg(self, msg):

		self.msg_image = self.font.render(self.text, True, self.text_color, \
													  self.color)
		self.msg_rect = self.msg_image.get_rect()
		self.msg_rect.center = self.rect.center

	def create_button(self):
		""" Button Factory """

		self.screen.fill(self.color, self.rect)
		self.screen.blit(self.msg_image, self.msg_rect)
		
		
		
		
		
		
		
