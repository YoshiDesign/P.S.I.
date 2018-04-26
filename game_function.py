
import pygame

import sys, os
from math import pi
from time import sleep
import requests
from multiprocessing import Process, Queue
from random import randint
from passlib.apps import custom_app_context as con_text
from analyze import Analyzer
from entity.explosion import Explosion
from entity.powerup import Powerup
from entity.bullets import Bullet
from entity.alien import Alien
from entity.tweeter import Tweeter

""" Username is a global var. Once we get the password we immediately auth w/ server """ 

# Data Relays to Thread_requests()
_relay_power = {'lazerup' : 0, 'bulletup' : 0, 'bombup' : 0, 'speedup' : 0}
_relay_score = {"points" : 0, "high_score" : 0, "multipliers" : 0}
_relay_other = {"dollars" : 0, "booster" : 0}


# unused currently
_offline = False
# This is the number of twits just blitted to the screen
total_twits = 0
# If acquired
get_lazer = False
get_bomb = False
# Timing constraints
laz_lok = 255
bom_lok = 255
# List of literal indices i.e. [1,3] means we destroyed 0 and 2 ...
twits_list = []
# List of full tweets
all_tweets = []
# initial screen state
cur_scrn = 0
# logged in
flagged = 0
# No names
names = ''
# DEBUG
test = 0
# unique
twit_id = 0
# Always weapon states
powers = {'gun' : 0 , 'lazerup' : 0, 'bulletup' : 0, 'bombup' : 0, 'scoreup' : 0}
difficulty = 0


def stat_keeper(_relay_power, _relay_score, _relay_other):
	""" Returns all data-trackers in a big ol' dict """
	pass


def check_events(g_settings, screen, ship, aliens, stats, \
									scores, projectiles):
	global get_lazer
	global laz_lok

	""" Tracks player events while game_active == True """

	# Used to ... ?
	mousex, mousey = pygame.mouse.get_pos()
	events = pygame.event.get()

	""" Plugging in the Clock-Pipe here ? """
	
	
	# Events : This wont run at the same time -event in events- occurs in textbox.update() via get_infoz
	for event in events:
		if event.type == pygame.QUIT:
			print("QUITS")
			return 'CE_QUIT'
		
		if event.type == pygame.KEYDOWN:
			keydown_event(event, g_settings, screen, ship, \
								stats, scores, projectiles)
			
			# if event.type == pygame.KEYUP:
			# keyup_event(event, g_settings, stats)

		elif event.type == pygame.KEYUP:
			keyup_event(event, g_settings, stats)
			

		elif laz_lok >= 254 and event.type == pygame.MOUSEBUTTONDOWN:
			
			if get_lazer:

				print("click_lazer")
				# Acquire "the lazer"
				lazers = projectiles[2]
				# Get level of "the lazer"
				laz_up = int(g_settings.lazer)
				# Fire "the lazer"
				fire_lazer(screen, g_settings, ship, lazers, laz_up)
				# Get_lazer will become redundant for precision
					
				return 0
	return 0

# UNUSED
def menu_keys(event):
	""" Only from main menu """
	# jic
	if not stats.game_active:
		#
		if event.key == pygame.K_b:
			# Offline play
			stats._current_screen = 3
			# scores.start_game(mode=0)

##########
# ADD ALT+Z TO TURN OFF UI
##########

def keyup_event(event, g_settings, stats):
	""" Keyups """
	# More events
	if stats.game_active:
		if event.key == pygame.K_d:
			g_settings.move_right = False
		elif event.key == pygame.K_a:
			g_settings.move_left = False
		elif event.key == pygame.K_s:
			g_settings.move_down = False
		elif event.key == pygame.K_w:
			g_settings.move_up = False
		elif event.key == pygame.K_SPACE:
			g_settings.firing = False
		elif event.key == pygame.K_q:
			g_settings.strafe_L = False
		elif event.key == pygame.K_e:
			g_settings.strafe_R = False
		elif event.key == pygame.K_SPACE:
			g_settings.firing = False

	return False

def keydown_event(event, g_settings, screen, ship, stats, 
					scores, projectiles, is_lazer=False):
	""" Keydowns """
	# Aka more events
	if stats.game_active:
		
		# Extra Boolean Falsey values included. Most recent key takes precedence in a pair

		if event.key == pygame.K_d:
			g_settings.move_left = False
			g_settings.move_right =  True

		elif event.key == pygame.K_a:
			g_settings.move_right = False
			g_settings.move_left =  True

		elif event.key == pygame.K_s:
			g_settings.move_up = False
			g_settings.move_down = True

		elif event.key == pygame.K_w:
			g_settings.move_down = False
			g_settings.move_up = True

		elif event.key == pygame.K_SPACE:
			g_settings.firing = True
			# Handles bullets and bombs
			fire_weapon(g_settings, screen, ship, projectiles[1], projectiles[0])

	return 0

def fire_weapon(g_settings, screen, ship, bullets, bombs):

	global powers
	global bom_lok
	global get_bomb

	k_boom = 	powers['bombup'] 	= g_settings.bomb
	k_bull = 	powers['bulletup'] 	= g_settings.bullets

	# Fire upgraded bullets
	if powers['bulletup']:
		# Shuts off the main gun
		g_settings.default_gun = 0
		powers['gun'] = 0
		fire_bullets(screen, g_settings, ship, bullets, k_bull, v='bulletup')

	# Fire bombs (also k_SPACE)
	if powers['bombup'] and bom_lok >= 250:
		# If not bomblock
		if (len(bombs.sprites()) < 3 and k_boom == 1) or \
			(len(bombs.sprites()) < 3 and k_boom == 2) or \
			(len(bombs.sprites()) < 3 and k_boom == 3):
			fire_bomb(screen, g_settings, ship, bombs, k_boom, v='bombup')

	# Fire default gun
	elif g_settings.default_gun:
		# We have the gun until we touch any bulletup
		powers['gun'] = 1
		if len(bullets.sprites()) <= 2:
			new_bullet = Bullet(g_settings, screen, ship, power='gun', level=1)
			bullets.add(new_bullet)

	return 0

def fire_lazer(screen, g_settings, ship, lazers, lazer_up):
	global laz_lok

	if laz_lok >= 243:
		print("FIRE! LAZER! {}", laz_lok)
		print("LAZERLEVEL ", g_settings.lazer)
		new_lazer = Bullet(g_settings, screen, ship, power='lazerup', level=lazer_up)
		lazers.add(new_lazer)

		g_settings.lazer, g_settings.lazer_ammo = \
		downgrade(g_settings.lazer, g_settings.lazer_ammo, mag=7, weap="laze")

		laz_lok = 0
	else:
		return 0

def fire_bullets(screen, g_settings, ship, bullets, k, v=''):

	for num in range(0, (k*2)):
		# k == 'bulletup' // v == v
		new_bullet = Bullet(g_settings, screen, ship, power=str(v), \
													  level=int(k), \
													  b_offset=num)
		bullets.add(new_bullet)

		# Spend ammo & check if weapon downgrades
		if k > 1:
			
			g_settings.bullets, g_settings.bullets_ammo, = \
			downgrade(g_settings.bullets, g_settings.bullets_ammo, mag=75, weap="bull")
			print("ammo AFTER downgrade ", g_settings.bullets_ammo)

		if g_settings.bullets == 1:
			num += 1
			# or we get 3 bullets at lvl 1 instead of 2 ... design choice
		if g_settings.bullets_ammo == 0:
			g_settings.bullets_ammo == 75
			
	return True

def fire_bomb(screen, g_settings, ship, bomb, k, v=''):
	global bom_lok
	if bom_lok >= 243:

		for num in range(2):
			new_bomb = Bullet(g_settings, screen, ship, power=str(v), \
														  level=int(k), \
														  b_offset=num)
			bomb.add(new_bomb)
			bom_lok = 0

			if k > 1:
				g_settings.bomb, g_settings.bomb_ammo, = \
				downgrade(g_settings.bomb, g_settings.bomb_ammo, mag=10, weap='bomb')
			if g_settings.bomb_ammo == 0:
				g_settings.bomb_ammo == 10

def downgrade(weapon, ammo, mag=0, weap=''):

	""" Discards spent ammo. weap is only for debugging """

	if weapon > 1:
		
		if ammo <= 0:
			print("spending weapon!! -- {} {}".format(ammo, weap))
			weapon -= 1
			print(" WEAPON DOWNGRADED {}".format(weapon))
			ammo = int(mag * weapon)
			print("AMMO REFILLED {}".format(ammo))
			return (int(weapon), int(ammo))
		else:
			print("spending ammo -- {} {}".format(ammo, weap))
			ammo -= 1
			return (int(weapon), int(ammo))
	else:
		print("shooting lvl 1 weapon")
		# Required
		return 1, 0

def check_play_buttons(stats, textbox, buttons, cur_scrn=0, \
											mousex=0, mousey=0):

	""" 
		Enables user-click responses in any menu 
		Any True returned from here is to trigger textbox.update()
	"""

	global flagged

	# Check which game button was clicked. Defaults to False
	login_clicked = buttons[0].rect.collidepoint(mousex, mousey)
	about_clicked = buttons[1].rect.collidepoint(mousex, mousey)
	attack_clicked = buttons[2].rect.collidepoint(mousex, mousey)
	to_pass_clicked = buttons[3].rect.collidepoint(mousex, mousey)
	passed_clicked = buttons[4].rect.collidepoint(mousex, mousey)

	""" 
		cur_scrn = stats._current_screen

		0 : menu_mode
		1 : login_mode
		2 : pass_mode
		3 : In-Game
		4 : Logged in menu_mode
			
	"""

	if (login_clicked or attack_clicked \
	or about_clicked or to_pass_clicked \
	or passed_clicked) and not stats.game_active:
		# Reset game stats
		# stats.reset_all() ...It's in start_game
		
		if login_clicked and cur_scrn == 0:

			textbox.reset()
			# Change
			stats.login_mode()
			# reset state
			login_clicked = False
			return True

		if to_pass_clicked and cur_scrn == 1:

			# Change
			if not textbox.get_text():
				return False
			stats.pass_mode()
			# Reset state
			to_pass_clicked = False
			return True

		if passed_clicked and cur_scrn == 2:

			# Need to auth before flagged = 1

			if not len(textbox.get_text()):
				# Dont peek at the pw
				return False
			# Reset state
			passed_clicked = False

			return True

		elif (attack_clicked and textbox.get_text()) \
		and not stats.game_active and (cur_scrn == 0 or cur_scrn == 4):
			
			""" Fires when user clicks Attack w/ text entered """
			print("TWITTER MODE")
			return True

		elif about_clicked:
			print("bout")

	print("clickin")

	return False

def end_game(g_settings, screen, stats, ship, powerups, projectiles, \
					twits, scores, game_won=False, flagged=0):

	global total_twits
	global twits_list
	global all_tweets
	global twit_id
	global powers
	
	# Maybe I could reset globals at game start they could be used for score tracking
	total_twits = 0
	twits_list 	= []
	all_tweets 	= []
	twit_id 	= 0
	default_gun	= 1

	print(powers)
	# SHould reset at the beginning, not the end
	powers = {'gun' : 0, 'lazerup' : 0, 'bulletup' : 0, 'bombup' : 0}


	# Fuzz data from g_settings to Thread_requests()
	# Only 1 pipe-stream should be sent from here to Thread_rqsts


	for item in projectiles:
		item.empty()

	g_settings.set_special()
	twits.empty()
	powerups.empty()
	get_high_score(stats, scores)
	stats.reset_all()
	scores.prep_score()

	del(ship)
	
	stats.game_active = False
	# Flagged == User is logged in
	stats.menu_mode(flagged=flagged)
	

def reset_army(screen, twits):
	""" Place twits at the top of the screen """ 

	screen_rect = screen.get_rect()
	y = 1
	for n, twit in enumerate(twits):
		# print("n {}".format(n) )
		if not n % 10:
			y += 1

		twit.rect.x = screen_rect.left + twit.rect.width * n
		twit.rect.y = screen_rect.top + (twit.rect.height * y) + 20

def create_army(g_settings, screen, twits, all_tweets, \
										start=0, act=2):

	""" Blit 2 entire tweets to the screen """

	from re import findall
	global twit_list
	global total_twits
	global twit_id
	print(all_tweets)
	print("CREATING ARMY")

	re_palphaNum = r"^[a-zA-Z0-9'\"]+$"
	
	total_twits = 0
	dots 		= 0
	end_char 	= 0
	power 		= 0
	available_x = int(get_cols(g_settings))
	available_y = int(get_rows(g_settings))
	generate_x 	= make_space(available_x)
	generate_y 	= make_space(available_y)
	row 		= next(generate_y)
	# OPT does make sense to include in re_palphaNum then remove it by comparison?
	punct		= [",","\'","\"",".",":", ";", "?", "!"]

	# Unused. Will need!
	re_unicode	= r"[^\u0000-\u007F]"

	""" 
		Note : Row and column's incremental logic is 100% dissimilar 
					this supports dynamic twit allocation
	"""

	# OPT a better parsing method : for x in [i for i in tweet if i != re_palphaNum]

	# ROW is now 0
	for tweet in all_tweets[start:act]:

		# RT's are usually empty
		if "RT" in tweet or "rt" in tweet:
			continue

		# Assigns an ID unique to the whole tweet
		twit_id = twit_id + 1

		# That strange edgecase
		if "..." in tweet:
			tweet.remove("...")
		# Almost bubble sort
		tweet.append("...")

		# Separate words
		for word in tweet:
			word = word.lower()
			# Handles malformation
			if word == "...":
				word = "."
				dots = 1
			else:
				dots = 0

			# A (much too) thorough check
			if (findall(re_palphaNum, word)) \
			or dots:
				# Determine sentiment
				if word in Analyzer._neg_words:
		 			
		 			sentiment = 0
				else:
					sentiment = 1

				for n, letter in enumerate(word):
					# Skip punct
					if letter in punct:
						continue
					# Find if last letter
					if n == len(word) - 1 or dots:
						end_char = 1
					else:
						end_char = 0
					# Determines if carrying powerup			
					try:
						# Returns True if we just made the last char
						make = assign_twit(g_settings, screen, twits, letter, sentiment, \
													end_char, generate_x, row, twit_id)

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

		# Logical Grouping of all twits in a tweet

	row = next(generate_y)
	
	if len(all_tweets) >= 2:
		# print("CASE 1")
		# Destroy the first 2 tweets
		x = all_tweets.pop(0)
		x = all_tweets.pop(0)
		x = ""

	# Pop the last tweet if uneven tweets
	elif len(all_tweets):
		print("THERE ARE STILL TWEETS")
		x = all_tweets.pop(0)
		x='done!'

		print(x)

	return True

def assign_twit(g_settings, screen, twits, letter, sentiment, \
							end_char, generate_x, row, twit_id, \
														dots=0):
	""" 
		- Construct an individual character and its properties to be blasted.
		- 'dots' is a result of the Twitter API being handled by nltk tokenizer
		- Returns True if we should start a newline.
		- At the present, end_chars never contain power ups
	"""
	# Defaults
	global total_twits
	global twits_list

	x_pos = next(generate_x)
	# Is holding power up?
	powers = {
				'1' : 'bulletup', '2' : 'bombup', \
				'3' : 'lazerup', '4' : 'speedup', \
				'5' : 'bulletup', '6' : 'scoreup'
			}

	text_data = {}
	# If last char of a word
	text_data['end_char'] 	= int(end_char)\
	# Literal alphabetic char
	text_data['letter'] 	= str(letter.lower())
	# Pos or Neg
	text_data['sentiment'] 	= sentiment
	# Twit sequence num
	text_data['index']		= total_twits
	# Each twit belongs to a group (id); that being its tweet
	text_data['twit_id']	= int(twit_id)

	if not dots:
		
		character = Tweeter(g_settings, screen, \
							text_data=text_data)
		# Determine if carrying powerup
		x = randint(2,27)
		if not (x % 6):
			# Pick powerup
			x = randint(1,20)
			if x >= 6 and x < 11:
				# EASY DROP
				character.power = powers['6']
			elif x >= 18:
				character.power = powers['5']
			elif x < 18 and x > 11:
				character.power = powers['1']
			else:
				if not x == 2:
					x = randint(3,6)
				character.power = powers[str(x)]
		else:
			# twit does not have a power
			character.power = 0

		# Acquire placement
		give_twit_dimension(character, x_pos, row)
		twits.add(character)

		# Update globals
		twits_list.append(total_twits)
		total_twits += 1
		
	# Only text-wrap after we've printed a whole word
	if x_pos + 1 >= 40 and text_data["end_char"] == 1:
		del(text_data)
		return True

	elif text_data["end_char"] == 1:
		# Acquire the next location
		x_pos = next(generate_x)
		if letter == ".":
			# Add "..." character when necessary
			text_data["letter"] = "dots"
			text_data["index"] =  total_twits
			# Create Twit
			character = Tweeter(g_settings, screen, \
								text_data=text_data)
			give_twit_dimension(character, x_pos, row)
			# Update globals
			twits.add(character)
			total_twits += 1
			twits_list.append(total_twits)
			
		del(text_data)
		return False
	else:
		del(text_data)
		return False


### ### ### ### ### ### ### ### Twit Placement ### ### ### ### ### ### ### ### 

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
### ### ### ### ### ### ### ### ### Twitter mode Functions ### ### ### ### ### 

def get_high_score(stats, scores):
	""" Saves the high score """ 
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		scores.prep_high_score()
	return 0

### ### ### ### ### ### ### ### ### I AM A CLASS ### ### ### ### ### ### ###

def send_data_TEST(name, q, url=0, hash='', u_name='', flag=0):
	""" 
		flag = 0 = Activate the web server's view function to access the Twitter API 
		flag = 1 = Authenticate user from client login

	"""
	if not flag: # We are getting tweets
		resp = []
		url = "https://psigames.herokuapp.com/twit?h=" + name
		resp = requests.get(url)
		return q.put(resp.json())

	######## LOGIN #########
	elif flag: # We are logging the user in from menu
		ok = requests.post("https://psigames.herokuapp.com/servauth", \
								data={'hash':hash, 'u_name': u_name})
		if ok:
			return 1
		else:
			print("BADNESS == {} - {}".\
			format(ok.status_code, ok.reason))
			return 12


def get_infoz(g_settings, screen, twits, stats, scores, reticle, \
							textbox, buttons, cur_scrn=0, hide=0):
	""" 
		Check user input, get tweets from server, analyze them and begin game.
		textbox.update() returns True if use presses Enter 
	"""
	mousex, mousey = pygame.mouse.get_pos()
	pygame.mouse.set_visible(False)
	g_settings.set_special()
	reticle.blitme(mousex, mousey)
	
	events = pygame.event.get()
	if not cur_scrn or cur_scrn == 4:

		if mousex > 135 and mousey > 258 \
		and mousex < 351 and mousey < 312:
			# Login
			buttons[0].create_button()
		elif mousex > 827 and mousey > 258 \
		and mousex < 1068 and mousey < 320:
			# About
			buttons[1].create_button()
		elif mousex > 530 and mousey > 394 \
		and mousex < 690 and mousey < 452:
			# Attack
			buttons[2].create_button()
		""" 			In Main Menu			"""

		x1 = textbox.update(events, stats, textbox, buttons, mousex, mousey, cur_scrn=cur_scrn, hide=0)
		if x1 == 'TX_SEARCH':
			
			# handle is the user's input
			handle = textbox.get_text()

			if handle.lower() == "realdonaldtrump" or handle.lower() == "@realdonaldtrump":
				print("TRUUUUUUUMP")
				g_settings.is_Trump = True
			if handle.lower() == "yoshiyoshums" or handle.lower() == "@yoshiyoshums":
				print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOSHI")
				g_settings.is_Yoshi = True

			if not handle or handle == "":
				return False
			
			print("Getting tweets from @{}".format(handle))
			
			try:
				# Get Tweets from Twitter
				q = Queue()
				tweet_bot = Process(target=send_data_TEST, args=(handle, q), name="serv1", \
										kwargs={'flag':0, 'url':0, 'hash':'', 'u_name':''}, \
																				daemon=None)
				tweet_bot.start()

				i = 0
				# Loading Animation...
				while tweet_bot.is_alive():
					# OPT 
					i += 1
					colors = [((0), (255 - (i % 200)), (255 - (i % 200))), \
								((255 - (i % 200)), (0), (255 - (i % 200)))]

					loading_wheel(screen, i, reticle, colors)

					if i == 400:
						i = 0

				# Proc return
				tweet_bot.join()

				# The meat n' potatoes
				user_tweets = q.get()

			except: # Requests.exceptions or TimeoutError
				# Trace server exception to stderr
				print("Something went wrong : " \
				"{}".format(sys.exc_info()[:-1]))
				# ErrID
				return 11

### ### ### ### ### ### ### ### Tweet Tweet ### ### ### ### ### ### ### ### ###

			if user_tweets:
				# nothing is sacred ...
				global all_tweets
				# If Twitter API respond, load sentiment files
				positive = os.path.join(sys.path[0], \
						"sentiments/positive-words.txt")
				negative = os.path.join(sys.path[0], \
						"sentiments/negative-words.txt")

				# Sentiment Analyzer class
				analyzer = Analyzer(positive, negative, stats)

				# Create a list of analyzed tweets. Arbitrarily enumerated.
				for i, tweet in enumerate(user_tweets):
					"""
										all_tweets looks like:

						[["This", "is", "tweet", "one", "!"],["and", "two"]...etc]
					"""
					all_tweets.append(analyzer.analyze(tweet))

				# Setup game scenario
				global difficulty
				difficulty = int(analyzer.get_difficulty())
				
				create_army(g_settings, screen, twits, all_tweets)

				# Clean up our textbox
				textbox.reset()

				# Go
				scores.start_game(mode=1, handle=handle)
				
				return True

			# Or dont
			else:
				# Otherwise catch bad input
				print("Could not receive tweets from server")
				textbox.reset()
				
				""" INSERT OFFLINE GAME INSTEAD """

				return 13

		# Return signal to quit main program
		elif x1 == 'TX_QUIT':
			return 'TX_QUIT'

		else:
			# Display our text input field based on cur_scrn
			screen.blit(textbox.get_surface(), \
				((g_settings.screen_width//2) - 100, \
				(g_settings.screen_height//2) + 80))

			return False

### MENU BEHAVIORS ### 
	if cur_scrn == 1:

		global names

		""" 			In Username Menu			"""
		# OPT for readability a function could position our elements per page

		# Username Screen
		if mousex > 530 and mousey > 300:
			buttons[3].create_button()

		x2 = textbox.update(events, stats, textbox, \
							buttons, mousex, mousey, \
									cur_scrn=cur_scrn, hide=0)
		if x2 == 'TX_SEARCH':

			names = textbox.get_text()
			if not names:
				print('nothin here')
				return False

			stats.pass_mode()
			textbox.reset()
			print("U NAME == {}".format(names))

		elif x2 == 'TX_QUIT':
			return 'TX_QUIT'

		else:
			# Blit textbox on login screen
			screen.blit(textbox.get_surface(), \
				((g_settings.screen_width//2) - 100, \
				(g_settings.screen_height//2) - 200))

			return False

	if cur_scrn == 2:

		global flagged
		
		""" 			In Password Menu			"""

		if mousex > 530 and mousey > 300:
			buttons[4].create_button()
		x3 = textbox.update(events, stats, textbox, \
								buttons, mousex, mousey, \
									cur_scrn=cur_scrn, hide=1)
		if x3 == 'TX_SEARCH':

			x = textbox.get_text()
		
			# je moet je wachtwoord verbergen
			candy = textbox.hash_word()
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### #
### ### ### ### ###### ### ### ### ###### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

			if con_text.verify(x, candy):

				print("HASH COMPLETE ", candy)

				textbox.reset()
				# Send to server! WITH names
				############
				flagged = 1
				# SAVE NAME and BLIT TO MENU "You are logged in as :"
				#############
				stats.menu_mode(flagged=flagged)
				# update screen if auth

			else:

				return False

### ### ### ### ### ### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ###
### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ### ###				

		elif x3 == 'TX_QUIT':
			return 'TX_QUIT'

		else:
			# Blit textbox to password screen
			screen.blit(textbox.get_surface(), \
				((g_settings.screen_width//2) - 100, \
				(g_settings.screen_height//2) - 200))


		#### elif cur_scrn == 3: ABOUT PAGE
		#
		# 	screen.blit(textbox.get_surface(), \
		# ((g_settings.screen_width//4)*3-32, \
		# (g_settings.screen_height//6)*3-120))
		
		return False

def loading_wheel(screen, i, reticle, colors):
	""" PEP8 Pride """
	mousex, mousey = pygame.mouse.get_pos()
	reticle.blitme(mousex, mousey)
	pygame.display.flip()
	pygame.draw.aaline(screen, colors[0], [0, 560], [1200, 560], True)
	if i < 50:
		pygame.draw.aaline(screen, colors[i%2], [600, 560], [0, 550], True)
		pygame.draw.aaline(screen, colors[i%2], [600, 560], [1200, 550], True)
	elif i < 100:
		pygame.draw.aaline(screen, colors[i%2], [520, 560], [0, 520], True)
		pygame.draw.aaline(screen, colors[i%2], [680, 560], [1200, 520], True)
	elif i < 150:
		pygame.draw.aaline(screen, colors[i%2], [440, 560], [0, 490], True)
		pygame.draw.aaline(screen, colors[i%2], [760, 560], [1200, 490], True)
	elif i < 200:
		pygame.draw.aaline(screen, colors[i%2], [360, 560], [0, 460], True)
		pygame.draw.aaline(screen, colors[i%2], [840, 560], [1200, 460], True)
	elif i < 250:
		pygame.draw.aaline(screen, colors[i%2], [280, 560], [0, 430], True)
		pygame.draw.aaline(screen, colors[i%2], [920, 560], [1200, 430], True)
	elif i < 300:
		pygame.draw.aaline(screen, colors[i%2], [200, 560], [0, 410], True)
		pygame.draw.aaline(screen, colors[i%2], [1000, 560], [1200, 410], True)
	elif i < 350:
		pygame.draw.aaline(screen, colors[i%2], [120, 560], [0, 380], True)
		pygame.draw.aaline(screen, colors[i%2], [1080, 560], [1200, 380], True)
	elif i < 399:
		pygame.draw.aaline(screen, colors[i%2], [40, 560], [0, 350], True)
		pygame.draw.aaline(screen, colors[i%2], [1160, 560], [1200, 350], True)
	else:
		pygame.draw.aaline(screen, colors[i%2], [1, 560], [0, 350], True)
		pygame.draw.aaline(screen, colors[i%2], [1199, 560], [1200, 350], True)

def check_twit_edges(g_settings, twits):
	for twit in twits.sprites():

		if twit.check_edges():
			# Move these twits only
			move = twit.twit_id
			move_group = [t for t in twits.sprites() if t.twit_id == move]
			change_army_direction(g_settings, move_group)

def change_army_direction(g_settings, move_group):

	for i, twit in enumerate(move_group):

		if twit.rect.x > 600:
			# Edge buffer
			twit.rect.x -= 20

		elif twit.rect.x < 600:
			# Edge buffer
			twit.rect.x += 25

		twit.twit_direction *= -1
		twit.rect.y += g_settings.twit_drops

	return 0


def check_twit_bottom(screen, twits):

	screen_rect = screen.get_rect()
	for twit in twits.sprites():
		# Sprites in update_bullets() This might be useless <-- search "useless" to find all
		if twit.rect.bottom >= screen_rect.bottom - 100:
			print("TOUCHING BOTTOM")
			twits.remove(twit)
			return True
		else:
			return False

def update_twits(g_settings, screen, stats, ship, \
					powerups, twits, scores, projectiles):
	
	global test
	global all_tweets
	# active_ids = []

	if test != len(twits.sprites()):
		# DEBUGGING print tweets here
		#print("ALL TWEETS {}".format(all_tweets))
		print("=============================")
		test = len(twits.sprites())

	twits.update()

	# Check if twits touch edges
	check_twit_edges(g_settings, twits)

	if check_twit_bottom(screen, twits):

		ship_hit(g_settings, screen, stats, ship, powerups,\
						twits, scores, projectiles, bottom=1)
	
	# If twits hit the ship
	if pygame.sprite.spritecollideany(ship, twits):
		
		ship_hit(g_settings, screen, stats, ship, powerups, \
								twits, scores, projectiles)

	# Win Scenario
	if len(all_tweets) <= 1 and len(twits.sprites()) == 0:
		# REDUNDANT albeit safe
		end_game(g_settings, screen, stats, ship, powerups, projectiles, \
											twits, scores, game_won=True, \
															flagged=flagged)
	# Spawn Twits when there are 5 left standing
	elif len(twits.sprites()) <= 5 and len(all_tweets) > 1:
		# Instantiates the next 2-tweet militia
		create_army(g_settings, screen, twits, all_tweets)

	return 0

def ship_hit(g_settings, screen, stats, ship, powerups, \
						twits, scores, projectiles, bottom=0):
	
	global flagged
	global get_lazer
	global get_bomb

	get_lazer = False
	get_bomb = False

	# First, empty projectiles
	for item in projectiles:
			item.empty()
	# Second, worry about life
	if stats.ships_left > 0:

		# if bottom:
		reset_army(screen, twits)
		ship.center_ship()

		stats.ships_left -= 1
		print("SUBTRACTING LIFE")
		scores.prep_ships()
		powerups.empty()
		g_settings.init_dynamic_settings()
		ship.power_up()
	
		# Combination if init_dyn and ship.power_up will reset the ship.
	else:
		print("ENDING GAME")
		end_game(g_settings, screen, stats, ship, powerups, \
								projectiles, twits, scores, \
											flagged=flagged)

	return 0

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

#					""" ~~	~~	~~	~~''~~ ~~ ~~ ~~ ~~"""
#				    Love not too well the work of thy hands,
#						  Or the devices of thy heart.
#						      - J.R.R. Tolkein
#					"""									"""
	
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def spawn_powerup(g_settings, screen, powerups, the_pwr, the_pos):
	""" Create Powerups """
	new_power = Powerup(g_settings, screen, the_pwr, the_pos)
	powerups.add(new_power)
	return True

def check_kills(g_settings, screen, stats, twits, \
								members, powerups, \
											weapon=''):

	global twits_list
	global total_twits

	dead_twits = 0
	for twit in members:
		# Reduce health of twits
		if weapon == 'bullets':
			twit.health -= g_settings.bullet_dmg
		elif weapon == 'lazer':
			twit.health -= g_settings.lazer_dmg
		elif weapon == 'bomb':
			twit.health -= g_settings.bomb_dmg

		# If Dead
		if twit.health <= 0:

			try:# Deletes from screen & Sprite Group
				if twit.power:
					spawn_powerup(g_settings, screen, powerups, \
										twit.power, twit.rect)

				twits.remove(twit)
				# Update globals
				dead_twits += 1
				total_twits -= 1
				twits_list.remove(int(twit.index))

			# Trying to delete a twit simultaneously killed by another weapon
			except ValueError:
				return 0

	stats.score += (g_settings.twit_points * \
					g_settings.score_multi) * dead_twits
	return 0 

def update_bullets(g_settings, screen, stats, ship, scores, \
							projectiles, powerups, enter, exit, \
											aliens=0, twits=0):

	""" Bullet & Powerup events (add / remove / upgrade) """

	global twits_list
	global total_twits
	# OPT maybe just pass them by index to functions? These reassign every time
	bombs 	= projectiles[0]
	bullets = projectiles[1]
	lazers 	= projectiles[2]

	""" 
		There are several ways to determine an explosion. 
		i.e. use the global vars - determine where to mark 
		an explosion based upon which twit disappeared. 

		bullets is a general term, unfortunately. It could either
		be a bomb, lazer, bullet or gun projectile

	"""

	# REFAC
	bullets.update()
	powerups.update()
	lazers.update()
	bombs.update()
	# Flag

	# REFAC
	for item in projectiles:
		# Copy, because you cannot modify the sprite group WHILE iterating over it. Pygame constraint
		for proj in item.copy():
			if proj.rect.bottom <= 0 or proj.rect.top >= 800\
				or proj.rect.x <= 0 or proj.rect.x >= 1200:
				item.remove(proj)
	
	for power in powerups.copy():
		if power.rect.top > 800:
			powerups.remove(power)

	shot_down = pygame.sprite.groupcollide(bullets, twits, True, False)
	bomb_down = pygame.sprite.groupcollide(bombs, twits, True, False)
	laze_down = pygame.sprite.groupcollide(lazers, twits, False, False)
	
	# Shoosting
	if shot_down:
		""" specific to bullet hits """
		for members in shot_down.values():
			# Calculate score per kill and drop powerups
			check_kills(g_settings, screen, stats, twits, \
						members, powerups, weapon="bullets")
			break
		# Update Score
		scores.prep_score()
	if bomb_down:

		""" specific to bullet hits """
		for members in bomb_down.values():
			# Calculate score per kill and drop powerups
			check_kills(g_settings, screen, stats, twits, \
							members, powerups, weapon="bomb")
			break
		# Update Score
		scores.prep_score()
	if laze_down:
		""" specific to bullet hits """
		for members in laze_down.values():
			# Calculate score per kill and drop powerups
			check_kills(g_settings, screen, stats, twits, \
							members, powerups, weapon="lazer")
			break
		# Update Score
		scores.prep_score()

	""" insert other projectile instances here """

	# Powah
	get_power = pygame.sprite.spritecollideany(ship, powerups)
	if get_power: # The power

		# Changes apply to g_settings values
		# Initializes ship power from g_settings
		ship.power_up(pwr=apply_power(g_settings, stats, str(get_power.pwr), enter))

		powerups.remove(get_power)


def apply_power(g_settings, stats, get_power, enter):

	# OPT Hmmm...

	""" 
		Speedup is handled within Ship() class
		We send scoreup with lvl = current multiplier
		
	""" 
	global powers
	global get_lazer
	global get_bomb
	global default_gun


	print("applying {}".format(get_power))
	
	# Safety on 
	

	# OPT map power-up to numbers and return int instead of str
	# More efficient albeit less succinct

	if get_power == 'scoreup':
		stats.score += 15
		g_settings.score_multi += 0.05
		powers['scoreup'] = powers['scoreup'] + 1
		print("Cur score_mult {}".format(g_settings.score_multi))
		
	elif get_power == 'lazerup':

		get_lazer = True
		g_settings.lazer_ammo = 7

		if g_settings.lazer < 3:
			g_settings.lazer += 1
			powers['lazerup'] += 1

		if g_settings.lazer >= 3:
			g_settings.lazer = 3

			return False
		
	elif get_power == 'bulletup':
		print("BULLETS!")
		# Keeps gun disabled (redundant. See fire_weapon())
		powers['gun'] = 0
		if g_settings.bullets < 3:
			g_settings.bullets += 1
			
			# print("GSETTINGS BULLETS : {}\n \
			# 		powers[] BULLETS : {}\n\
			# 		ammo : {}".format(g_settings.bullets, powers['bulletup'], g_settings.bullets_ammo))

		if g_settings.bullets > 1:
			# Replenish Ammo
			g_settings.bullets_ammo = 75 * (g_settings.bullets)
			if g_settings.bullets_ammo >= 255 \
			and g_settings.bullets == 3:
				g_settings.bullets_ammo = 250

		if powers['bulletup'] < 3:
			powers['bulletup'] += 1

		if g_settings.bullets >= 3:
			g_settings.bullets = 3

			return False

	elif get_power == 'bombup':

		get_bomb = True
		if g_settings.bomb < 3:
			g_settings.bomb += 1
			powers['bombup'] += 1

		if g_settings.bomb > 1:
			g_settings.bomb_ammo = 10 * (g_settings.bomb)

		if g_settings.bomb >= 3:
			g_settings.bomb = 3

			return False
		
		### ### ### ### LISTENER ### ### ### ### 
		# 			Transmit powers
		### ### ### ### ### ? ### ### ### ### ### 
	return str(get_power)


def update_power_chart(screen, g_settings):

	# levels
	lazer_level = g_settings.lazer
	bullt_level = g_settings.bullets
	bombs_level = g_settings.bomb

	# ammos
	lazer_ammo 	= g_settings.lazer_ammo
	bullt_ammo	= g_settings.bullets_ammo
	bomb_ammo	= float(g_settings.bomb_ammo)

	if lazer_level:
		# print("BOMB LEVEL ", bombs_level)
		# print("BOMB AMMO ", bomb_ammo)
		if lazer_level >= 3:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1100, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1093, 478, 14, 14], 3)
			pygame.draw.line(screen, (255,255,255), [1100, 490], [1100, 565], 2)
			pygame.draw.rect(screen, (255,255,255), [1093, 565, 14, 14], 3)
			pygame.draw.line(screen, (255,255,255), [1100, 579], [1100, 579 + lazer_ammo * 10], 2)
			pygame.draw.rect(screen, (255,255,255), [1093, 652, 14, 14], 3)
		
		elif lazer_level >= 2:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1100, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1093, 478, 14, 14], 3)
			pygame.draw.line(screen, (255,255,255), [1100, 490], [1100, 490 + lazer_ammo * 10], 2)
			pygame.draw.rect(screen, (255,255,255), [1093, 565, 14, 14], 3)

		elif lazer_level >= 1:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1100, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1093, 478, 14, 14], 3)
		
		
	if bullt_level:

		if bullt_level >= 3:
			# Level 1
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1067, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1053, 478, 14, 14], 3)
			# Level 2 w/o scaling
			pygame.draw.line(screen, (255,255,255), [1060, 490], [1060, 565], 2)
			pygame.draw.rect(screen, (255,255,255), [1053, 565, 14, 14], 3)
			# Level 3
			pygame.draw.line(screen, (255,255,255), [1060, 579], [1060, 579 + (bullt_ammo // 3 - 4)], 2)
			pygame.draw.rect(screen, (255,255,255), [1053, 652, 14, 14], 3)

		elif bullt_level >= 2:
			# Level 1
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1067, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1053, 478, 14, 14], 3)
			# Level 2
			pygame.draw.line(screen, (255,255,255), [1060, 490], [1060, 490 + bullt_ammo // 2], 2)
			pygame.draw.rect(screen, (255,255,255), [1053, 565, 14, 14], 3)

		elif bullt_level >= 1:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1067, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1053, 478, 14, 14], 3)
	
	if bombs_level:
		
		if bombs_level >= 3:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1133, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1133, 478, 14, 14], 3)
			pygame.draw.line(screen, (255,255,255), [1140, 490], [1140, 565], 2)
			pygame.draw.rect(screen, (255,255,255), [1133, 565, 14, 14], 3)
			pygame.draw.line(screen, (255,255,255), [1140, 579], [1140, 579 + bomb_ammo * 2.0 + 10], 2)
			pygame.draw.rect(screen, (255,255,255), [1133, 652, 14, 14], 3)
		
		elif bombs_level >= 2:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1133, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1133, 478, 14, 14], 3)
			pygame.draw.line(screen, (255,255,255), [1140, 490], [1140, 490 + bomb_ammo * 3.3 + 5], 2)
			pygame.draw.rect(screen, (255,255,255), [1133, 565, 14, 14], 3)

		elif bombs_level >= 1:
			pygame.draw.line(screen, (255,255,255), [1100, 424], [1133, 478], 2)
			pygame.draw.rect(screen, (255,255,255), [1133, 478, 14, 14], 3)
		

	return 0

def weapon_locks(screen, mousex, mousey, get_lazer, get_bomb):
	""" Responsible for reticles and lazer/bomb lockouts """

	global laz_lok
	global bom_lok

	if get_lazer:
		if not laz_lok < 200:
			laz_lok = 255
		else:
			laz_lok += 3

	if get_bomb:
		if not bom_lok < 245:
			bom_lok = 255
		else:
			bom_lok += 200

	if not laz_lok == 255:
		pygame.draw.aalines(screen, (5 * (laz_lok % 50), 0, 0), False, \
					[[mousex + 11,mousey],[mousex, mousey - 11], \
					[mousex, mousey - 11],[mousex - 11, mousey], \
					[mousex - 11, mousey],[mousex, mousey + 11], \
					[mousex, mousey + 11],[mousex + 11, mousey]], False)

	else:
		pygame.draw.aalines(screen, (255, 10, 255), False,\
					[[mousex + 11, mousey],[mousex,mousey - 11], \
					[mousex, mousey - 11],[mousex - 11, mousey], \
					[mousex - 11, mousey],[mousex, mousey + 11], \
					[mousex, mousey + 11],[mousex + 11, mousey]], False)

	if not bom_lok == 255:
		pygame.draw.aalines(screen, (255, 0, 0), False, \
					[[mousex + 11, mousey],[mousex - 11, mousey], \
					[mousex + 8, mousey - 3],[mousex - 8, mousey - 3], \
					[mousex + 5, mousey - 5],[mousex - 5, mousey - 5], \
					[mousex + 3, mousey - 8],[mousex - 3, mousey - 8]], False)

	return 0

def update_screen(g_settings, screen, font, ship, textbox, aliens, reticle, \
					twits, powerups, projectiles, stats, scores, buttons):

	# JUST FOR DEBUGGING
	global cur_scrn
	global flagged
	global get_lazer
	global get_bomb
	global difficulty
	
	# JUST FOR DEBUGGING
	if not cur_scrn == stats._current_screen:
		cur_scrn = stats._current_screen
		print("cur scrn == {}".format(stats._current_screen))
	mousex, mousey = pygame.mouse.get_pos()
	# Load current background
	g_settings.load_background(screen, display=stats._current_screen)
	
	if stats.game_active:
		if difficulty:
			screen.blit(font.render(str(difficulty), True, (255,255,255)), (115, 745))

		if stats._current_screen == 3:
			scores.show_score()
			update_power_chart(screen, g_settings)
			# Might not need this here
			# global all_tweets

			if get_lazer or get_bomb:
				# Paint Reticle to screen in-game
				weapon_locks(screen, mousex, mousey, get_lazer, get_bomb)

			twits.draw(screen)

			# OPT only needs to draw bullets / gun
			for item in projectiles:

				for projectile in item.sprites():
					projectile.draw_projectile()

			for power in powerups.sprites():
				power.blitme()

			ship.update()

	else: # Menu contexts
		if stats._current_screen == 2:
			if get_infoz(g_settings, screen, twits, \
						stats, scores, reticle,textbox, buttons, \
							cur_scrn=stats._current_screen, hide=1) == 'TX_QUIT':
				return 'TX_QUIT'
		else:
			if get_infoz(g_settings, screen, twits, \
					stats, scores, reticle, textbox, buttons, \
								cur_scrn=stats._current_screen) == 'TX_QUIT':
				return 'TX_QUIT'

	pygame.display.flip()
