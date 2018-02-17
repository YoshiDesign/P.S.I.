import pygame
import sys, os
import multiprocessing
from time import sleep
import requests
from analyze import Analyzer
from entity.bullets import Bullet
from entity.alien import Alien
	
def check_events(g_settings, screen, ship, aliens, stats, textbox, play_twit_btn, play_reg_btn):
	""" Displays text input box as well as monitors player events """

	events = pygame.event.get()
	if not stats.game_active:
		# Activates text box
		get_infoz(events, g_settings, screen, ship, stats, textbox)
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

				# OP : check_play_buttons and check_player_clicks could be 1 functions
				# as the conditions for check_play_buttons, arent entirely verbose

				print("oyo")
				check_play_buttons(events, g_settings, screen, ship, stats, textbox, play_reg_btn, \
					play_twit_btn, aliens, mousex, mousey)

			else:
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
		
		if btn_reg_clicked:
			print("REGULAR MODE")
			# Start reg
			stats.start_game()
			
			
		elif (btn_twit_clicked and textbox.get_text()) or textbox.get_text():
			print("TWITTER MODE")
			# Start twitter

			stats.start_game(game="tw")
			


		elif btn_twit_clicked and not textbox.update(events):
			print("NOPE")
		else:
			print("NUTHIN BUT DEBUGGIN")

		# reset ship
		# reset reticle

def start_twit_game(g_settings, screen, ship, aliens, stats):
	
	# Switch_game sets class property
	ship.switch_game()
	aliens.switch_game()

	print("SHIP {}".format(ship._current_game))
	#bullets.switch_game()


def create_army(g_settings, screen, ship, tweet_bot):
	""" Create our Twitter Foes""" 



def update_army():
	pass

def set_Classes():
	pass
	
def check_player_clicks(g_settings, screen, ship, stats, mousex, mousey):
	""" Click """
	pass
	
	
def send_data_TEST(name, fail=0):
	""" Activate the web server's view function to access the Twitter API """
	resp = []
	url = "https://sleepy-river-27272.herokuapp.com/twit?h=" + name
	resp = requests.get(url)
	return resp.json()

	
def get_infoz(events, g_settings, screen, ship, stats, textbox):
	""" 
		This function's modularity is in its order 
		of operations as opposed to ad-hoc functions
	"""
	##
	# events = pygame.event.get()
	# Continue to monitor since we are not multiprocessing yet
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
	
	if textbox.update(events):
		
		# handle is the user's input
		handle = textbox.get_text()
		print("Getting tweets from @{}".format(handle))

		# No interruptions but still traceback to stderr
		try:
			tweet_bot = send_data_TEST(handle)
		except:
			# If the tweets did not make it we get falsey
			print("Something went wrong : {}".\
				format(sys.exc_info()[:-1]))
			return False

		if tweet_bot:
			# If Twitter API responds
			tokenized_tweets = []
			# Get (probably) POSIX paths to txt files
			positive = os.path.join(sys.path[0], \
					"sentiments/positive-words.txt")
			negative = os.path.join(sys.path[0], \
					"sentiments/negative-words.txt")
			analyzer = Analyzer(positive, negative, stats)

			for i, tweet in enumerate(tweet_bot):
				"""
					Tweets are stored in a list as the analysis occurs.
								List looks like:
					[["This", "is", "tweet", "one", "!"],["and", "two"]...etc]
				"""
				tokenized_tweets.append(analyzer.analyze(tweet))

			print(tokenized_tweets)
			print(analyzer._pos_words)
			create_army(g_settings, screen, ship, tweet_bot)
			stats.switch_game()
			stats.game_active = True
			return True
		# Secondary Error catch should we somehow bypass exception
		else:
			print("Could not receive tweets from server")
			return False
	else:
		# Display our text input and gather user input
		x, y = g_settings.screen_width // 4, g_settings.screen_height // 6
		screen.blit(textbox.get_surface(), (x*3-100, y*3-80))
		return False

def update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
						 stats, play_reg_btn, play_twit_btn):
	# Mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()
	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen)
	
	if stats.game_active:
		# if _current_game is true...
		if stats._current_game:
			# ...A twitter-mode game started
			ship.update(game_type=1)
		else:
			ship.update()
			reticle.blitme(mouse_x, mouse_y)
			aliens.blitmeh()
	else:
		play_reg_btn.create_button()
		play_twit_btn.create_button()
		# If everything breaks
		






	
	
	
	
