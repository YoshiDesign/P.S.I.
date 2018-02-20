import pygame
import sys, os
import multiprocessing
from time import sleep
from collections import OrderedDict as OD
import requests
from analyze import Analyzer
from entity.bullets import Bullet
from entity.alien import Alien
from entity.tweeter import Tweeter
	
def check_events(g_settings, screen, ship, aliens, stats, textbox, twits, play_twit_btn, play_reg_btn):
	""" Displays text input box as well as monitors player events """

	events = pygame.event.get()
	if not stats.game_active:
		# Activates text box
		get_infoz(events, g_settings, screen, ship, twits, stats, textbox)
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

def check_play_buttons(events, g_settings, screen, ship, \
							stats, textbox, play_reg_btn, \
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
			stats.twit_active = True
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

	print("SHIP {}".format(ship._current_game))
	#bullets.switch_game()


	return True

def get_align_x(g_settings, entity):
	pass

def get_align_y(g_settings, entity):
	pass

def update_army():
	pass

def align_army():
	enemy = Tweeter(g_settings, screen)
	pass
	
def check_player_clicks(g_settings, screen, ship, aliens, stats, mousex, mousey):
	""" Click """
	pass


def create_army(g_settings, screen, twits, tokenized, \
							neg_words, pos_words, start=0,act=3):

	import re
	end_char = 0
	text_data = {}
	available_x = int(get_cols(g_settings))
	available_y = int(get_rows(g_settings))
	re_alphaNum = r"^[a-zA-Z0-9 ]+$"
	# I should add !  ? and *

	# [start:act] control how many & which tweets are made

	position_x = make_space(available_x)
	position_y = make_space(available_y)
	y = next(position_y)

	for tweet in tokenized[start:act]:
		print(tweet)

		for word in tweet:

			

			if re.search(re_alphaNum, word):

				if word in Analyzer._neg_words:
		 			# insert POD RACER
		 			print("NEGATORY {}".format(word))
		 			sentiment = 0
				else:
					sentiment = 1

				for n, letter in enumerate(word):

					# Identify the last char of word
					if n == len(word) - 1:
						end_char = 1
					else:
						end_char = 0
					"""
						Create our twit army
					"""
					# create_twit(end_char, letter, sentiment, available_x, available_y)
					# Instantiate generators
					text_data["end_char"] = int(end_char)
					text_data["letter"] = str(letter.lower())
					text_data["sentiment"] = str(sentiment)
					

					character = Tweeter(g_settings, screen, text_data=text_data)

					try:
						width = character.rect.width
						# Using our generators we can assign a specific location to each letter

						character.x = width * next(position_x)
						character.rect.x = character.x
						character.rect.y = character.rect.height + (2 * (character.rect.height * y))
						twits.add(character)

						# If we are towards to right edge and at the end of a word
						if next(position_x) >= 45 and text_data["end_char"] == 1:
							y = next(position_y)
							position_x = make_space(available_x)

################################
################################
################################

						if text_data["end_char"] == 1:

							text_data["letter"] = "space"
							character = Tweeter(g_settings, screen, text_data=text_data)
							width = character.rect.width
							# Using our generators we can assign a specific location to each letter
							character.x = width * next(position_x)
							character.rect.x = character.x
							character.rect.y = character.rect.height + (2 * (character.rect.height * y))
							twits.add(character)
						
							

					# When we run out of X positions to assign in a row
					except StopIteration:
						# We move to the next row down, and start from position 0
						y = next(position_y)
						position_x = make_space(available_x)


			else:
				continue

		y = next(position_y)

	# Clean up
	text_data = {}

# Generator from 0 to total COLS
def make_space(columns):
	for space in range(columns):
		yield space

def get_cols(g_settings):
	cols = int(g_settings.screen_width // int(g_settings.char_width))
	print("COLS {}".format(cols))
	print("GSET CHAR WIDTH {}".format(g_settings.char_width))
	avail_space = int(cols * g_settings.char_width - (8 * int(g_settings.char_width)))
	print(avail_space)
	return int(avail_space)

def get_rows(g_settings):
	avail_space = float(g_settings.screen_height - (5 * g_settings.char_height))
	return avail_space
		
def update_twits(g_settings, screen, stats, twits):
	twits.update()
	
def send_data_TEST(name, fail=0):
	""" Activate the web server's view function to access the Twitter API """
	resp = []
	url = "https://sleepy-river-27272.herokuapp.com/twit?h=" + name
	resp = requests.get(url)
	return resp.json()


def get_infoz(events, g_settings, screen, ship, twits, stats, textbox):
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
			# If the tweets did not make it we get falsey >> terminal
			print("Something went wrong : {}".format(sys.exc_info()[:-1]))
				
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
							tokenized_tweets looks like:
					[["This", "is", "tweet", "one", "!"],["and", "two"]...etc]
				"""
				tokenized_tweets.append(analyzer.analyze(tweet))

			# Safe to use direct call to analyzer_words here ...fully endorsed
			create_army(g_settings, screen, twits, tokenized_tweets, \
							analyzer._neg_words, \
							analyzer._pos_words)
			stats.switch_game()
			stats.game_active = True
			return True
		# Secondary Error catch should we somehow bypass an erroneous server response
		else:
			print("Could not receive tweets from server")
			return False
	else:
		# Display our text input and gather user input
		x, y = g_settings.screen_width // 4, g_settings.screen_height // 6
		screen.blit(textbox.get_surface(), (x*3-100, y*3-80))
		return False

def update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
							twits, stats, play_reg_btn, play_twit_btn):
	# Mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()
	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen)
	
	if stats.game_active:
		# if _current_game is true...
		if stats._current_game:
			# ...A twitter-mode game started
			# print("starting twitter mode")
			ship.update(game_type=1)
			twits.draw(screen)
		else:
			ship.update()
			reticle.blitme(mouse_x, mouse_y)
			# aliens.blitmeh()
	else:
		play_reg_btn.create_button()
		play_twit_btn.create_button()
		# If everything breaks

	pygame.display.flip()
		






	
	
	
	
