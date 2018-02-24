import pygame
import sys, os
from time import sleep
import requests

from analyze import Analyzer
from entity.explosion import Explosion
from entity.bullets import Bullet
from entity.alien import Alien
from entity.tweeter import Tweeter

# unused
_offline = False
# Initial deletion of blank twits
dropped_space = 1

total_twits = 0
# List of literal indices
twits_list = []
# List of full tweets
all_tweets = []
# Arbitrary
flag_1 = 0
	
def check_events(g_settings, screen, ship, aliens, stats, textbox, scores, \
						twits, bullets, play_twit_btn, play_reg_btn):
	""" Tracks text input box and all player events """

	events = pygame.event.get()
	if not stats.game_active:
		# Activates text box
		pass
	# Events
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
		# If textinput.update() == True, user pressed Return
		elif event.type == pygame.MOUSEBUTTONDOWN:
			print("click")

			mousex, mousey = pygame.mouse.get_pos()
			print("x y".format(mousex, mousey))

			if not stats.game_active:
				# OP : check_play_buttons and check_player_clicks could be 1 functions
				# as the conditions for check_play_buttons, arent entirely verbose
				check_play_buttons(events, g_settings, screen, ship, twits, \
														stats, textbox, \
														scores, play_reg_btn, \
														play_twit_btn, aliens, \
														mousex=mousex, mousey=mousey)
			else:
				check_player_clicks(g_settings, screen, ship, aliens, stats, mousex, mousey)

		elif event.type == pygame.KEYDOWN:
			keydown_event(event, g_settings, screen, ship, stats, scores, bullets)
			if not stats.game_active:
				check_play_buttons(events, g_settings, screen, ship, twits, stats, textbox, scores, play_reg_btn, \
																			play_twit_btn, aliens)

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

def keydown_event(event, g_settings, screen, ship, stats, scores, bullets):
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
		elif event.key == pygame.K_b:
			stats._current_game = 0
			scores.start_game(mode=0)

def check_play_buttons(events, g_settings, screen, ship, twits, \
							stats, textbox, scores, play_reg_btn, \
							play_twit_btn, aliens, mousex=0, mousey=0):
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
			scores.start_game(mode=0)
			# scores.start_game()
			
		elif (btn_twit_clicked and textbox.get_text()) and not stats.game_active:
			""" Fires when user clicks instead of pressing Enter """

			print("TWITTER MODE")
			# Start twitter
			get_infoz(events, g_settings, screen, ship, twits, stats, scores, textbox, clicked=1)
			
			
		elif btn_twit_clicked and not textbox.update(events):
			print("NOPE")
		else:
			print("BUG CHECK btn_reg_clicked == {}\n btn_twit_clicked == {}\n {}")

		# reset ship
		# reset reticle

def check_player_clicks(g_settings, screen, ship, aliens, stats, mousex, mousey):
	""" Click """
	pass


def end_game(g_settings, screen, stats, scores):

	stats.game_active = False
	stats.reset_all()
	scores.prep_score()
	stats.base_mode()
	x, y = g_settings.screen_width // 4, g_settings.screen_height // 6
	# screen.blit(textbox.get_surface(), (x*3-100, y*3-80))


def reset_army(screen, twits):
	""" Place twits at the top of the screen """ 
	print("Resetting Army")
	screen_rect = screen.get_rect()
	y = 1
	for n, twit in enumerate(twits):
		# print("n {}".format(n) )
		if not n % 8:
			y += 1
			# print("Y % 60 {}".format(y))

		twit.rect.x = screen_rect.left + twit.rect.width * n
		twit.rect.y = screen_rect.top + (twit.rect.height * y) + 20


def create_army(g_settings, screen, twits, all_tweets, \
										start=0, act=2):

	import re
	global twit_list
	# start = int(start)
	# act = int(act)
	re_alphaNum = r"^[a-zA-Z0-9]+$"
	re_ascii	= r"[^\u0000-\u007F]"
	re_nother	= r"(?<=\u0000-\u007F)[a-Z0-9]"
	punct		= [",","'","\"",".",":"]
	dots 		= 0
	end_char 	= 0
	available_x = int(get_cols(g_settings))
	available_y = int(get_rows(g_settings))
	generate_x 	= make_space(available_x)
	generate_y 	= make_space(available_y)
	row = next(generate_y)
	# print(all_tweets)
	# ROW is assigned because unlike X, it is not reset, it has a stable vector throughout.
	# ROW is now 0
	for tweet in all_tweets[start:act]:
		# Get rid of the confusing bits
		if "..." in tweet:
			tweet.remove("...")
		#if wild in tweet:
			#tweet.remove(wild)

		# Add our own delimiter
		tweet.append("...")

		# print("TWEET {}".format(tweet))
		for word in tweet:
			# 3 simple flag checks are not worth an 
			# extra function on the stack frame imo

			word = word.lower()
			# FLAG : if tweet cut off
			if word == "...":
				word = "."
				# print("DOTS {}".format(word))
				dots = 1
			else:
				dots = 0

			if (re.findall(re_alphaNum, word) and word.isalpha()) or dots:

				if word in Analyzer._neg_words:
		 			# FLAG : determine sentiment
		 			sentiment = 0
				else:
					sentiment = 1

				for n, letter in enumerate(word):
					# FLAG : Identify the last char of the word
					if letter in punct:
						continue
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
			else:
				continue

	# Destroy the first 2 tweets
	x = all_tweets.pop(0)
	x = all_tweets.pop(0)
	x = ""

	row = next(generate_y)


	""" 		NOT TO BE CONFUSED WITH UPDATE_TWIT
		This returns a tweet, or searches exhaustively and gives up
										 					"""
	# RECONSIDER this placement? Should be a separate function
	# This looks for more tweets to create the army with. It is recursive
	if total_twits == 0:
		if len(all_tweets) == 0:
			# Destroy the tweets we just blasted and tidy up
			print("Tweets Exhausted")
			# TODO -- Ask for another Handle? or submit score. Or both
			return False
		else:
			create_army(g_settings, screen, twits, all_tweets)
	

def assign_twit(g_settings, screen, twits, letter, sentiment, \
							end_char, generate_x, row, dots=0):
	""" Construct an individual character and its properties to be blasted.
		'dots' is a result of the Twitter API being handled by the nltk tokenizer """
	# Defaults
	global total_twits
	global twits_list
	x_pos = next(generate_x)
	text_data = {}
	text_data["end_char"] 	= int(end_char)
	text_data["letter"] 	= str(letter.lower())
	text_data["sentiment"] 	= sentiment
	text_data["space"] 		= 0
	text_data["index"]		= total_twits
	
	print("assinging Tweet")

	# Using our generators we can systematically assign each letter
	if not dots:
		
		character = Tweeter(g_settings, screen, text_data=text_data)
		give_twit_dimension(character, x_pos, row)
		twits.add(character)

		total_twits += 1
		twits_list.append(total_twits - 1)

		#print("TWIT 000 STUFF {}\n{}".format(total_twits, twits_list))

	# Only text-wrap after we've printed a whole word
	if x_pos + 1 >= 40 and text_data["end_char"] == 1:
		return True
	elif text_data["end_char"] == 1 or dots:
		# Acquire the next location
		x_pos = next(generate_x)
		# Enter data for a space character
		text_data["letter"] = "space"
		text_data["space"] = 1

		# Could be an Ordered Dict too..
		if dots:
			text_data["space"] = 0
			text_data["letter"] = "dots"
			text_data["index"] =  total_twits
			total_twits += 1
			twits_list.append(total_twits - 1)

		# Make a space char
		character = Tweeter(g_settings, screen, text_data=text_data)
		give_twit_dimension(character, x_pos, row)
		twits.add(character)

		

		# print("TWIT 2 STUFF {}\n{}".format(total_twits, twits_list))
		return False
	else:
		# If the character created is not last in the word
		return False

	# Hats off to ye'
	del(text_data)
### ### ### ### ### ### ### ### Tweet Placement ### ### ### ### ### ### ### ### 

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


### ### ### ### ### ### ### ### ### Twitter mode Functions ### ### ### ### ### 

def change_army_direction(g_settings, twits):

	for twit in twits.sprites():
		# Space Buffer
		if twit.rect.x > 600:
			twit.rect.x -= 5
		elif twit.rect.x < 600:
			twit.rect.x += 5
		twit.rect.y += g_settings.twit_drop_speed
	g_settings.twit_direction *= -1

def update_twits(g_settings, screen, stats, ship, \
					twits, scores, bullets, init=0):

	global dropped_space
	global all_tweets
	twits.update()
	# Check if twits touch edges
	check_twit_edges(g_settings, twits)
	check_twit_bottom(g_settings, stats, scores, screen, ship, twits, bullets)
	# If twits hit the ship
	
	if pygame.sprite.spritecollideany(ship, twits): # and not twit.letter == "space":
		
		ship_hit(g_settings, screen, stats, ship, twits, scores, bullets)

	# dropped_space global, this will only occur once and remove all empty space placeholders
	if dropped_space:
		print("DROPPING SPACE CHARS")
		dropped_space = 0
		for twit in twits.sprites():

			if twit.letter == "space":
				print("{}".format(twit.letter))
				twits.remove(twit)

	print(len(twits.sprites()))

	# DONT NOTICE ME!
	global flag_1
	# DIFFICULTY SETTING -> 5
	# PROBLEM - this is also activating when we ship_hit due to twit.empty()
	if len(twits.sprites()) <= 5:
		dropped_space = 0
		# Instantiates the next 2-tweet militia
		create_army(g_settings, screen, twits, all_tweets)
	return 0


### ### ### ### ### ### ### ### ### ### NETWORK ### ### ### ### ### ### ### ###

def check_twit_bottom(g_settings, stats, scores, screen, ship, twits, bullets):
	screen_rect = screen.get_rect()
	for twit in twits.sprites():
		# The "not twit.letter == space" should be unnecessary. We removed all space
		# Sprites in update_bullets() This might be useless <-- search "useless" to find all
		if twit.rect.bottom >= screen_rect.bottom and not twit.letter == "space":
			ship_hit(g_settings, screen, stats, ship, twits, scores, bullets, bottom=1)
			break

def ship_hit(g_settings, screen, stats, ship, twits, scores, bullets, bottom=0):
	global flag_1
	global dropped_space
	if stats.ships_left > 0:
		if bottom:
			reset_army(screen, twits)
		stats.ships_left -= 1
		scores.prep_ships()
		bullets.empty()
		ship.center_ship()

	else:
		# Game Over
		flag_1 = 1
		dropped_space = 0
		twits.empty()
		bullets.empty()
		get_high_score(stats, scores)
		end_game(g_settings, screen, stats, scores)

	ship.center_ship()

def get_high_score(stats, scores):
	""" Saves the high score """ 
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		scores.prep_high_score()

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def send_data_TEST(name, fail=0):
	""" Activate the web server's view function to access the Twitter API """
	resp = []
	url = "https://sleepy-river-27272.herokuapp.com/twit?h=" + name
	resp = requests.get(url)
	return resp.json()

def get_infoz(events, g_settings, screen, ship, twits,\
					 stats, scores, textbox, clicked=0):
	""" 
		This function's modularity is in its order 
		of operations as opposed to ad-hoc functions
		Enjoy
	"""
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()

	# If player presses ENTER or clicks the Twitter button
	if textbox.update(events) or clicked:
		
		# handle is the user's input
		handle = textbox.get_text()
		if not handle or handle == "":
			return False
		
		print("Getting tweets from @{}".format(handle))
		# No interruptions but still traceback to stderr
		try:
			tweet_bot = send_data_TEST(handle)
		except:
			# Any erroneous or otherwise NULL returns
			print("Something went wrong : " \
			"{}".format(sys.exc_info()[:-1]))
				
			return False

		if tweet_bot:
			global all_tweets
			# If Twitter API responds
			# Get (probably) POSIX paths to txt files
			positive = os.path.join(sys.path[0], \
					"sentiments/positive-words.txt")
			negative = os.path.join(sys.path[0], \
					"sentiments/negative-words.txt")
			analyzer = Analyzer(positive, negative, stats)

			for i, tweet in enumerate(tweet_bot):
				"""
					Tweets are stored in a list as the analysis occurs.
							all_tweets_tweets looks like:
					[["This", "is", "tweet", "one", "!"],["and", "two"]...etc]
				"""
				all_tweets.append(analyzer.analyze(tweet))

			# Safe to use direct call to analyzer_words here ...fully endorsed
			create_army(g_settings, screen, twits, all_tweets)
			textbox.reset()
			scores.start_game(mode=1, handle=handle)
			
			return True
		# Secondary Error catch should we somehow bypass an erroneous server response
		else:
			
			print("Could not receive tweets from server")
			# BLIT MSG TO SCREEN, "Play offline instead? Y/N"
			""" THIS IS WHERE WE BEGIN AN OFFLINE GAME """
			return False
	else:
		# Display our text input and gather user input
		x, y = g_settings.screen_width // 4, g_settings.screen_height // 6
		screen.blit(textbox.get_surface(), (x*3-100, y*3-80))
		return False

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
def fire_bullets(g_settings, screen, ship, bullets):
	if len(bullets) < 40:
		# Make bullets
		new_bullet = Bullet(g_settings, screen, ship)
		bullets.add(new_bullet)

def update_bullets(g_settings, screen, stats, ship, scores,  \
										 bullets, powerup, aliens=0, twits=0):
	""" Bullet events (add / remove / upgrade)"""
	global twits_list
	global total_twits

	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	if stats._current_game:
		shot_down = pygame.sprite.groupcollide(bullets, twits, True, True)
	else:
		shot_down = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if shot_down:
		
		for bull, twit in shot_down.items():
			# print("SDV == {}".format(shot_down.values()))
			# print("TWIT {}".format(twit))
			#for i in twits: since it's a weird container type returned by groupcollide
			for i in twit:
				# spaces were removed about 15 lines up, this might be useless
				if not i.letter == "space":
					explode = Explosion(g_settings, screen, i)
					explode.explode()
					twits_list.remove(int(i.index))
					total_twits -= 1
					# print("TWIT UPDATE {}\n{}\n\n".format(total_twits, twits_list))
			stats.score += g_settings.twit_points * len(twit)
			# print("SCORE {}".format(stats.score))
		scores.prep_score()

def update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
										twits, bullets, stats, scores, \
											play_reg_btn, play_twit_btn):
	# Mouse
	mouse_x, mouse_y = pygame.mouse.get_pos()
	pygame.mouse.set_visible(False)
	reticle.blitme(mouse_x, mouse_y)
	pygame.display.flip()

	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen, game=stats._current_game)
	
	if stats.game_active:
		# if _current_game is true...
		if stats._current_game:
			# ...A twitter-mode game started
			# print("starting twitter mode")
			ship.update(game_type=1)
			twits.draw(screen)
			for bullet in bullets.sprites():
				bullet.draw_bullet()

		elif not stats._current_game:
			ship.update(game_type=0)
			# aliens.blitmeh()

		scores.show_score()

	else:
		play_reg_btn.create_button()
		play_twit_btn.create_button()

		events = pygame.event.get()
		get_infoz(events, g_settings, screen, ship, twits, stats, scores, textbox)

		# If everything breaks
	# print("LEN OF TWITS = {}".format(len(twits)))
