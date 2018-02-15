import pygame
import sys
import multiprocessing
from time import sleep
import requests
from bullets import Bullet
from alien import Alien
	
def check_events(g_settings, screen, ship, aliens, stats, textbox, play_twit_btn, play_reg_btn):

	events = pygame.event.get()

	# Events
	for event in events:
		print(event)

		if event.type == pygame.QUIT:
			sys.exit()
		# If textinput.update() == True, user pressed Return
		elif event.type == pygame.MOUSEBUTTONDOWN:

			mousex, mousey = pygame.mouse.get_pos()
			print("oy")
			if not stats.game_active:
				print("oy")
				check_play_buttons(events, g_settings, screen, ship, stats, textbox, play_reg_btn, \
					play_twit_btn, aliens, mousex, mousey)
			else:
				# Check Clicks during Gameplay
				check_player_clicks(g_settings, screen, ship, aliens, stats, mousex, mousey)
		elif event.type == pygame.KEYDOWN:
			keydown_event(event, g_settings, screen, ship, stats)
		elif event.type == pygame.KEYUP:
			keyup_event(event, ship, stats)
			
def keyup_event(event, ship, stats):
	""" Keyups """
	# More events
	if stats.game_active:
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
	# Aka more events
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

def check_play_buttons(events, g_settings, screen, ship, stats, textbox, play_reg_btn, \
					play_twit_btn, aliens, mousex, mousey):
	""" 
		Check specifically for button presses 
		Only Callable while game_active = 0
	"""

	# Check which game mode was selected
	btn_reg_clicked = play_reg_btn.rect.collidepoint(mousex, mousey)
	btn_twit_clicked = play_twit_btn.rect.collidepoint(mousex, mousey)

	if (btn_reg_clicked or btn_twit_clicked) and not stats.game_active:
		stats.reset_all()
		check = textbox.update(events)
		if btn_reg_clicked and not stats._current_game:
			print("REGULAR")
			# Start reg
			stats.start_game()
			
			
		elif btn_twit_clicked or check:
			print("YUP")
			# Start twitter

			stats.start_game(game="tw")
			start_twit_game(g_settings, screen, ship, aliens, stats)


		elif btn_twit_clicked and not textbox.update(events):
			print("NOPE")
		else:
			print("NUTHIN BUT DEBUGGIN")

		# reset ship
		# reset reticle

def start_twit_game(g_settings, screen, ship, aliens, stats):
	
	ship.switch_game()
	print("SHIP {}".format(ship._current_game))
	aliens.switch_game()
	#bullets.switch_game()

	



def set_Classes():
	pass
	
def check_player_clicks(g_settings, screen, ship, aliens, stats, mousex, mousey):
	""" Click """
	pass
	
	
def send_data_TEST(name, fail=0):
	resp = []
	url = "https://sleepy-river-27272.herokuapp.com/twit?h=" + name
	resp = requests.get(url)
	
	return resp.json()

	
def get_infoz(g_settings, screen, ship, stats, textbox):
	""" Bring textbox to screen and monitor input """
	events = pygame.event.get()
	# Continue to monitor since we are not multiprocessing yet
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
	if textbox.update(events):

		# handle = User Input
		handle = textbox.get_text()

		#start_twit_game(g_settings, screen, ship, stats)

		# Get Twitter timeline, needs multiprocess capability
		x = send_data_TEST(handle)
		print(x)
		### ### ### ### ### ### ### ### ### ###

					# ANALYZER


		### ### ### ### ### ### ### ### ### ###
		stats.game_active = True
		stats.game_twit_active = True

		return False
	else:
		x, y = g_settings.screen_width // 4, g_settings.screen_height // 4
		screen.blit(textbox.get_surface(), (x*3-100, y*3-80))
		return False


def update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
						 stats, play_reg_btn, play_twit_btn):
	# Mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()
	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen)
	
	if stats.game_active:
		ship.update()
		reticle.blitme(mouse_x, mouse_y)
		aliens.blitmeh()
	else:
		play_reg_btn.create_button()
		play_twit_btn.create_button()
		# If everything breaks
		






	
	
	
	
