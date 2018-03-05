import pygame, os


class Reticle():
	
	def __init__(self, g_settings, screen):
		
		self.screen = screen
		self.fp_lazer = os.fsencode("media/sprites/reticle/")
		self.g_settings = g_settings
		# Mouse
		self.image = pygame.image.load(os.fsdecode(self.fp_lazer) + "Lazer_Reticle.png").convert_alpha()
		self.rect = self.image.get_rect()
		
	def blitme(self, x, y):
		self.rect.centerx = x
		self.rect.centery = y
		self.screen.blit(self.image, self.rect)
		
