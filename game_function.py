import pygame
import sys
from time import sleep

from bullets import Bullet
from alien import Alien

def update_screen(g_settings, screen, ship):
	
	screen.blit(g_settings.background, g_settings.background_rect)
	
	pygame.display.flip()
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
