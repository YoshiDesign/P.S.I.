import pygame
import sys
from time import sleep

from bullets import Bullet
from alien import Alien


	
def check_events(g_settings, screen, ship, stats):

	events = pygame.event.get()

	for event in events:
		print(event)

		if event.type == pygame.QUIT:
			sys.exit()
		# If textinput.update() == True, user pressed Return
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
	
	
def send_data():
	pass
	
def update_screen(g_settings, screen, ship, aliens, ret, stats):
	# Mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()
	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen)
	
	if stats.game_active:
		ship.update()
		ret.blitme(mouse_x, mouse_y)
		aliens.blitmeh()

	
def get_infoz(g_settings, screen, ship, stats, textbox):
	""" Bring textbox to screen and monitor input """
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
	if textbox.update(events):
		# handle = User Input
		handle = textbox.get_text()
		print("HANDLE {}".format(len(handle)))
		start_game(g_settings, screen, ship, stats)
	
	else:
		screen.blit(textbox.get_surface(), (g_settings.screen_width / 2, 10))


def start_game(g_settings, screen, ship, stats):
	
	# Reset score / lvl / lives
	stats.reset_stats()
	stats.game_active = True
	pygame.mouse.set_visible(False)
	#ship.center_ship()
	#g_settings.change_reticle()
	
	
	
	
