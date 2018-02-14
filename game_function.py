import pygame
import sys
from time import sleep

from bullets import Bullet
from alien import Alien


	
def check_events(g_settings, screen, ship, stats):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mousex, mousey = pygame.mouse.get_pos()
			check_player_clicks(event, g_settings, screen, ship)
			
		elif event.type == pygame.KEYDOWN:
			keydown_event(event, g_settings, screen, ship, stats)
		elif event.type == pygame.KEYUP:
			keyup_event(event, ship)
			
def keyup_event(event, ship):
	""" Keyups """
	if event.key == pygame.K_d:
		ship.move_right = False
	elif event.key == pygame.K_a:
		ship.move_left = False
	elif event.key == pygame.K_s:
		ship.move_down = False
	elif event.key == pygame.K_w:
		ship.move_up = False

def keydown_event(event, g_settings, screen, ship, stats):
	""" Keydowns """
	if stats.game_active:
		if event.key == pygame.K_d:
			ship.move_right = True
		elif event.key == pygame.K_a:
			ship.move_left = True
		elif event.key == pygame.K_s:
			ship.move_down = True
		elif event.key == pygame.K_w:
			ship.move_up = True
		elif event.key == pygame.K_SPACE:
			pass
		elif event.key == pygame.K_b:
			start_game(g_settings, screen, stats, ship)
		
	
def check_player_clicks(event, g_settings, screen, ship):
	""" Click """
	pass
	
	
	
def update_screen(g_settings, screen, ship):
	
	g_settings.load_background(screen)
	ship.update()
	pygame.display.flip()
	
	
def start_game(g_settings, screen, stats):
	
	# Reset score / lvl / lives
	stats.reset_stats()
	stats.game_active = True
	#g_settings.change_reticle()
	
	
	
	
