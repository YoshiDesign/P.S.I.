import pygame
import sys, os
import multiprocessing
from time import sleep
import requests

from analyze import Analyzer
from entity.explosion import Explosion
from entity.bullets import Bullet
from entity.alien import Alien
from entity.tweeter import Tweeter
	
def check_events(g_settings, screen, ship, aliens, stats, textbox, twits, bullets, play_twit_btn, play_reg_btn):
	""" Tracks text input box and all player events """

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
			keydown_event(event, g_settings, screen, ship, stats, bullets)
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

def keydown_event(event, g_settings, screen, ship, stats, bullets):
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
			fire_bullets(g_settings, screen, ship, bullets)

def check_play_buttons(events, g_settings, screen, ship, \
							stats, textbox, play_reg_btn, \
							play_twit_btn, aliens, mousex, mousey):
	""" 
		Checks for our button activity
		Only Callable while game_active = 0
	"""
	# Check which game mode was selected
	btn_reg_clicked = play_reg_btn.rect.collidepoint(mousex, mousey)
	btn_twit_clicked = play_twit_btn.rect.collidepoint(mousex, mousey)

	if (btn_reg_clicked or btn_twit_clicked) and not stats.game_active:

		# Reset game stats
		stats.reset_all()
		
		if btn_reg_clicked:
			print("REGULAR MODE")
			# Start reg
			stats.start_game()
			
		elif (btn_twit_clicked and textbox.get_text()) or textbox.get_text():
			print("TWITTER MODE")
			# Start twitter
			stats.switch_game()
			stats.start_game()
			
		elif btn_twit_clicked and not textbox.update(events):
			print("NOPE")
		else:
			print("BUG CHECK btn_reg_clicked == {}\n btn_twit_clicked == {}\n {}")

		# reset ship
		# reset reticle

def check_player_clicks(g_settings, screen, ship, aliens, stats, mousex, mousey):
	""" Click """
	pass

def ship_hit(g_settings, screen, stats, ship, twits):
	sys.exit()

def fire_bullets(g_settings, screen, ship, bullets):
	if len(bullets) < 40:
		# Make bullets
		new_bullet = Bullet(g_settings, screen, ship)
		bullets.add(new_bullet)

def create_army(g_settings, screen, twits, tokenized, \
							neg_words, pos_words, start=0,act=3):

	import re
	re_alphaNum = r"^[a-zA-Z0-9 ]+$"
	# Idk what 'wild' is, hopefully it doesn't cause portability errors
	wild 		= '…'
	wild2		= '...'
	dots 		= 0
	end_char 	= 0
	available_x = int(get_cols(g_settings))
	available_y = int(get_rows(g_settings))
	generate_x 	= make_space(available_x)
	generate_y 	= make_space(available_y)
	row = next(generate_y)
	# ROW is assigned because unlike X, it is not reset, it has a stable vector throughout.
	# ROW is now 0
	for tweet in tokenized[start:act]:
		# Get rid of the confusing bits
		if wild2 in tweet:
			tweet.remove(wild2)
		if wild in tweet:
			tweet.remove(wild)

		# Add our own delimiter
		tweet.append("...")

		print("TWEET {}".format(tweet))
		for word in tweet:

			# 3 simple flag checks are not worth an 
			# extra function on the stack frame imo

			word = word.lower()
			# FLAG : if tweet cut off
			if word == "...":
				word = "."
				print("DOTS {}".format(word))
				dots = 1
				
			if re.search(re_alphaNum, word) or dots:

				if word in Analyzer._neg_words:
		 			# FLAG : determine sentiment
		 			sentiment = 0
				else:
					sentiment = 1

				for n, letter in enumerate(word):
					# FLAG : Identify the last char of the word
					if n == len(word) - 1:
						end_char = 1
					else:
						end_char = 0					
					try:
						make = assign_twit(g_settings, screen, twits, letter, sentiment, \
													end_char, generate_x, row, dots=dots)

						if make or dots: # (Is the last char and >= position 40)
							# Carriage return + newline
							generate_x = make_space(available_x)
							row = next(generate_y)
							dots = 0

					except StopIteration:
						""" This more than likely wont incur from the above algo"""
						row = next(generate_y)
						position_x = make_space(available_x)

	row = next(generate_y)

def assign_twit(g_settings, screen, twits, letter, sentiment, end_char, generate_x, row, dots=0):
	""" Construct an individual character and its properties to be displayed.
		'dots' is a result of the Twitter API being handled by the nltk tokenizer """
	# Defaults
	x_pos = next(generate_x)
	text_data = {}
	text_data["end_char"] 	= int(end_char)
	text_data["letter"] 	= str(letter.lower())
	text_data["sentiment"] 	= sentiment
	text_data["space"] 		= 0

	# Using our generators we can systematically assign each letter
	if not dots:
		character = Tweeter(g_settings, screen, text_data=text_data)
		give_twit_dimension(character, x_pos, row)
		twits.add(character)
	# Only text-wrap after we've printed a whole word
	if x_pos + 1 >= 40 and text_data["end_char"] == 1:
		return True
	elif text_data["end_char"] == 1 or dots:
		# Acquire the next location
		x_pos = next(generate_x)
		# Enter data for a space character
		text_data["letter"] = "space"
		text_data["space"] = 1
		if dots:
			text_data["letter"] = "dots"
		# Make a space char
		character = Tweeter(g_settings, screen, text_data=text_data)
		give_twit_dimension(character, x_pos, row)
		twits.add(character)
		return False
	else:
		# If the character created is not last in the word
		return False
	# Hats off to ye'
	del(text_data)

def give_twit_dimension(character, x_pos, row):
	""" Tells each character where to appear on screen """
	width = character.rect.width
	character.x = width * x_pos
	character.rect.x = character.x
	character.rect.y = character.rect.height + (2 * (character.rect.height * row))

# Generator from 0 to total COLS
def make_space(columns):
	for space in range(columns):
		yield space

def get_cols(g_settings):
	cols = int(g_settings.screen_width // int(g_settings.char_width))
	avail_space = int(cols * g_settings.char_width - (2 * int(g_settings.char_width)))
	return int(avail_space)

def get_rows(g_settings):
	avail_space = float(g_settings.screen_height - (2 * int(g_settings.char_height)))
	return avail_space

def check_twit_edges(g_settings, twits):
	for twit in twits.sprites():
		if twit.check_edges():
			change_army_direction(g_settings, twits)

def change_army_direction(g_settings, twits):

	for twit in twits.sprites():
		# Space Buffer
		twit.rect.x += 5
		twit.rect.y += g_settings.twit_drop_speed
	g_settings.twit_direction *= -1

def update_twits(g_settings, screen, stats, ship, twits):
	twits.update()
	# Check if twits touch edges
	check_twit_edges(g_settings, twits)
	# If twits hit the ship
	if pygame.sprite.spritecollideany(ship, twits):
		ship_hit(g_settings, screen, stats, ship, twits)

### ### ### ### ### ### ### ### ### ### NETWORK ### ### ### ### ### ### ### ### ### ### ### ### ###

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

def update_bullets(g_settings, screen, stats, ship, twits, bullets):
	""" Bullet events (add / remove / upgrade)"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	shot_down = pygame.sprite.groupcollide(bullets, twits, True, True)

	if shot_down:
		
		for twit in shot_down.values():
			print("TWIT {}".format(twit))
			explode = Explosion(g_settings, screen, twit)
			explode.explode()
			stats.score += g_settings.twit_points * len(twit)
			print("SCORE {}".format(stats.score))


def update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
							twits, bullets, stats, play_reg_btn, play_twit_btn):
	# Mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()

	pygame.display.flip()
	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen)

	for bullet in bullets.sprites():
		bullet.draw_bullet()

	
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