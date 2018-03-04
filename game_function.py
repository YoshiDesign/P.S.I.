
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


# unused currently
_offline = False
# Live count of active letters
total_twits = 0
# List of literal indices
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
	
def check_events(g_settings, screen, ship, aliens, stats, \
							textbox, scores, twits, bullets):

	""" Tracks text input box and all player events while game_active == True """


	mousex, mousey = pygame.mouse.get_pos()
	events = pygame.event.get()

	# Events : This wont run at the same time event in events occurs in textbox.update() in get_infoz
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
		# If textinput.update() == True, user pressed Return
		elif event.type == pygame.MOUSEBUTTONDOWN:
			print("click, you glorious bitch, CLICK!")
			
			# mousex, mousey = pygame.mouse.get_pos()
			
		elif event.type == pygame.KEYDOWN:
			keydown_event(event, g_settings, screen, ship, stats, \
													scores, bullets)

		elif event.type == pygame.KEYUP:
			keyup_event(event, g_settings, ship, stats)

	return 0
	
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

def keyup_event(event, g_settings, ship, stats):
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


	return False



def keydown_event(event, g_settings, screen, ship, stats, scores, \
															bullets):
	""" Keydowns """
	# Aka more events
	if stats.game_active:

		if event.key == pygame.K_d:
			g_settings.move_right = True
		elif event.key == pygame.K_a:
			g_settings.move_left = True
		elif event.key == pygame.K_s:
			g_settings.move_down = True
		elif event.key == pygame.K_w:
			g_settings.move_up = True
		elif event.key == pygame.K_SPACE:
			fire_bullets(g_settings, screen, ship, bullets)
		

	return False

def check_play_buttons(stats, textbox, scores, buttons, cur_scrn=0, \
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
			# Change Screens
			stats.login_mode()
			# reset state
			login_clicked = False
			return True

		if to_pass_clicked and cur_scrn == 1:

			# Change Screens
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

def check_player_clicks(g_settings, screen, ship, aliens, stats, \
													mousex, mousey):
	""" Click """
	pass

def end_game(g_settings, screen, stats, ship, powerups, twits, bullets, scores, \
										game_won=0, flagged=0):

	global dropped_space
	global total_twits
	global twits_list
	global all_tweets
	if game_won:
		pass
		# SET FLAG FOR STUFF
	###
	#
	#	SEND STATS TO SERVER
	#
	###


	

	total_twits = 0
	twits_list = []
	all_tweets = []

	bullets.empty()
	twits.empty()
	powerups.empty()
	get_high_score(stats, scores)
	stats.reset_all()

	scores.prep_score()
	
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

	re_palphaNum = r"^[a-zA-Z0-9'\"]+$"
	dots 		= 0
	end_char 	= 0
	power 		= 0
	available_x = int(get_cols(g_settings))
	available_y = int(get_rows(g_settings))
	generate_x 	= make_space(available_x)
	generate_y 	= make_space(available_y)
	row 		= next(generate_y)
	punct		= [",","\'","\"",".",":", ";", "?", "!"]
	# Unused. Will need!
	re_unicode	= r"[^\u0000-\u007F]"

	""" 
		Note : Row and column's incremental logic is 100% dissimilar 
					this supports dynamic twit allocation
	"""

	# ROW is now 0
	for tweet in all_tweets[start:act]:

		# RT's are usually empty
		if "RT" in tweet or "rt" in tweet:
			continue


		g_settings.twit_id += 1
		twit_id = g_settings.twit_id

		# That strange edge-case
		if "..." in tweet:
			tweet.remove("...")
		# Trust me on this
		tweet.append("...")

		# print("TWEET {}".format(tweet))
		for word in tweet:
			word = word.lower()
			# Handles a particular malformation
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
					if n == len(word) - 1:
						end_char = 1
					else:
						end_char = 0
					# Determines if carrying powerup			
					try:
						# Returns True if we just made the last c
						make = assign_twit(g_settings, screen, twits, letter, sentiment, \
													end_char, generate_x, row, twit_id, \
																			dots=dots)

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
	total_twits = 0
	if len(all_tweets) >= 2:
		# Destroy the first 2 tweets
		x = all_tweets.pop(0)
		x = all_tweets.pop(0)
		x = ""

	# Pop the last tweet if uneven tweets
	elif len(all_tweets):
		x = all_tweets.pop(0)
		x='done!'

	return False

def assign_twit(g_settings, screen, twits, letter, sentiment, \
							end_char, generate_x, row, twit_id, \
														dots=0):
	""" 
		Construct an individual character and its properties to be blasted.
		'dots' is a result of the Twitter API being handled by the nltk tokenizer 
	"""
	# Defaults
	global total_twits
	global twits_list

	x_pos = next(generate_x)
	# Is holding power up?
	power = 0
	text_data = {}
	# If last char of a word
	text_data["end_char"] 	= int(end_char)\
	# Literal
	text_data["letter"] 	= str(letter.lower())
	# Pos or Neg
	text_data["sentiment"] 	= sentiment
	# Twit sequence num
	text_data["index"]		= total_twits
	# Each twit belongs to a group (id); that being its tweet
	text_data["twit_id"]	= twit_id

	if not dots:
		
		character = Tweeter(g_settings, screen, \
							text_data=text_data)
		# Determine if carrying powerup
		x = randint(1,26)
		if not (x % 5):
			# DIFFICULTY SETTING
			character.power = randint(1, 5)
		else:
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

	elif text_data["end_char"] == 1 or dots:
		# Acquire the next location
		x_pos = next(generate_x)
		if dots:
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

def check_twit_edges(g_settings, twits):
	for twit in twits.sprites():
		if twit.check_edges():
			change_army_direction(g_settings, twits, twit.twit_id)

def change_army_direction(g_settings, twits, twit_id):

	for i, twit in enumerate(twits.sprites()):
		if twit.power:
			print("{} has powerup {}".format(i, twit.power))
		# Space Buffer
		if twit.twit_id == twit_id:

			if twit.rect.x > 600:
				twit.rect.x -= 15
			elif twit.rect.x < 600:
				twit.rect.x += 15
			twit.rect.y += g_settings.twit_drop_speed
			twit.twit_direction *= -1

def update_twits(g_settings, screen, stats, ship, \
			powerups, twits, scores, bullets, init=0):
	
	global test
	global all_tweets
	# active_ids = []

	if test != len(twits.sprites()):
		# DEBUGGING print tweets here
		test = len(twits.sprites())

	twits.update()

	# Check if twits touch edges
	check_twit_edges(g_settings, twits)
	if check_twit_bottom(g_settings, stats, scores, screen, \
										ship, twits, bullets):

		ship_hit(g_settings, screen, stats, ship, powerups,\
							twits, scores, bullets, bottom=1)
	
	# If twits hit the ship
	if pygame.sprite.spritecollideany(ship, twits):
		
		ship_hit(g_settings, screen, stats, ship, powerups, \
										twits, scores, bullets)

	# DONT NOTICE ME!
	
	# DIFFICULTY SETTING -> 5
	# PROBLEM - this is also activating when we ship_hit due to twit.empty()
	if len(all_tweets) == 0 and not total_twits:
		end_game(g_settings, screen, stats, ship, powerups,\
					twits, bullets, scores, flagged=flagged)

	elif len(twits.sprites()) <= 5 and len(all_tweets) >= 1:
		# Instantiates the next 2-tweet militia
		create_army(g_settings, screen, twits, all_tweets)

	return 0


### ### ### ### ### ### ### ### ### ### NETWORK ### ### ### ### ### ### ### ###

def check_twit_bottom(g_settings, stats, scores, screen, \
									ship, twits, bullets):
	screen_rect = screen.get_rect()
	for twit in twits.sprites():
		# Sprites in update_bullets() This might be useless <-- search "useless" to find all
		if twit.rect.bottom >= screen_rect.bottom:
			return True
		else:
			return False

def ship_hit(g_settings, screen, stats, ship, powerups, \
						twits, scores, bullets, bottom=0):
	
	global flagged

	if stats.ships_left > 0:
		if bottom:
			reset_army(screen, twits)
		stats.ships_left -= 1
		scores.prep_ships()
		bullets.empty()
		ship.center_ship()
		powerups.empty()
		g_settings.init_dynamic_settings()
		ship.power_up()

	else:
		end_game(g_settings, screen, stats, ship, powerups, \
				twits, bullets, scores, flagged=flagged)

	return 0

def get_high_score(stats, scores):
	""" Saves the high score """ 
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		scores.prep_high_score()
	return 0

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

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


def get_infoz(g_settings, screen, twits,\
				stats, scores, reticle, textbox, buttons, \
										cur_scrn=0, hide=0):
	""" 
		Check user input, get tweets from server, analyze them and begin game.
		textbox.update() returns True if use presses Enter 
	"""


	mousex, mousey = pygame.mouse.get_pos()
	print(mousex, mousey)
	pygame.mouse.set_visible(False)
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
		""" 			In Main Menu					"""
        
       
		if textbox.update(events, stats, textbox, \
							scores, buttons, mousex, mousey, \
									cur_scrn=cur_scrn, hide=0):
		
			# handle is the user's input
			handle = textbox.get_text()
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
				# Loading ...

				while tweet_bot.is_alive():
					i += 1
					colors = [((0), (255 - (i % 200)), (255 - (i % 200))), \
								((255 - (i % 200)), (0), (255 - (i % 200)))]

					print('loading')

					loading_wheel(screen, i, reticle, colors)

					if i == 400:
						i = 0

				del(i)
				tweet_bot.join()

				# The meat n' potatoes
				user_tweets = q.get()

			except: # Requests.exceptions or TimeoutError
				# Trace server exception to stderr
				print("Something went wrong : " \
				"{}".format(sys.exc_info()[:-1]))
				# ErrID
				return 11

			if user_tweets:
				# nothing is sacred
				global all_tweets
				# If Twitter API responds
				# Get (probably) POSIX paths to txt files
				positive = os.path.join(sys.path[0], \
						"sentiments/positive-words.txt")
				negative = os.path.join(sys.path[0], \
						"sentiments/negative-words.txt")
				analyzer = Analyzer(positive, negative, stats)

				# Not 100% sure why I enumerated this.
				for i, tweet in enumerate(user_tweets):
					"""
						Tweets are stored in a list as the analysis occurs.
								all_tweets_tweets looks like:
						[["This", "is", "tweet", "one", "!"],["and", "two"]...etc]
					"""
					all_tweets.append(analyzer.analyze(tweet))

				# Begin Game
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
			# Display our text input field based on cur_scrn
			screen.blit(textbox.get_surface(), \
				((g_settings.screen_width//2) - 100, \
				(g_settings.screen_height//2) + 80))

	if cur_scrn == 1:
		global names

		""" 			In Username Menu			"""

		# Username Screen
		if mousex > 530 and mousey > 300:
			buttons[3].create_button()
		if textbox.update(events, stats, textbox, \
							scores, buttons, mousex, mousey, \
									cur_scrn=cur_scrn, hide=0):

			names = textbox.get_text()
			if not names:
				print('nothin here')
				return False

			stats.pass_mode()
			textbox.reset()
			print("U NAME == {}".format(names))

		else:
			# Blit textbox on login screen
			screen.blit(textbox.get_surface(), \
				((g_settings.screen_width//2) - 100, \
				(g_settings.screen_height//2) - 200))

	if cur_scrn == 2:
		global flagged
		
		""" 			In Password Menu			"""
		if mousex > 530 and mousey > 300:
			buttons[4].create_button()
		if textbox.update(events, stats, textbox, \
							scores, buttons, mousex, mousey, \
									cur_scrn=cur_scrn, hide=1):

			x = textbox.get_text()
		
			# je moet je wachtwoord verbergen
			candy = textbox.hash_word()

			if con_text.verify(x, candy):
				print("WOOOOOOOT")

			
			textbox.reset()
			# Send to server! WITH names
			############
			flagged = 1
			# SAVE NAME and BLIT TO MENU "You are logged in as :"
			#############
			stats.menu_mode(flagged=flagged)
			# update screen if auth

		else:
			# Blit textbox to password screen
			screen.blit(textbox.get_surface(), \
				((g_settings.screen_width//2) - 100, \
				(g_settings.screen_height//2) - 200))


		#### elif cur_scrn == 3:
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


	



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
def fire_bullets(g_settings, screen, ship, bullets):
	if len(bullets) < 40:
		# Make bullets
		new_bullet = Bullet(g_settings, screen, ship)
		bullets.add(new_bullet)
		return 0
	else:
		return False

def check_kills(g_settings, screen, stats, bullets, members, twits, powerups):

	global twits_list
	global total_twits

	dead_twits = 0
	for twit in members:
		twit.health -= 1
		if twit.health == 0:
			if twit.power:
				# Spawn any powerups
				print("I HAVE THE POWAH {}".format(twit.power))
				spawn_powerup(g_settings, screen, powerups, twit)

			# Delets from screen & Sprite Group
			twits.remove(twit)
			# Update globals
			dead_twits += 1
			twits_list.remove(int(twit.index))

	total_twits -= dead_twits
	stats.score += g_settings.twit_points * dead_twits

	return True 

def update_bullets(g_settings, screen, stats, ship, scores, \
						bullets, powerups, aliens=0, twits=0):
	""" Bullet & Powerup events (add / remove / upgrade) """

	global twits_list
	global total_twits

	""" 
		There are several ways to determine an explosion. 
		i.e. use the global vars - determine where to mark 
		an explosion based upon which twit disappeared. 
	"""

	# If they drift off-screen
	# OPT Could use a daemon thread for these 2
	bullets.update()
	powerups.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	for power in powerups.copy():
		if power.rect.top > 800:
			powerups.remove(power)


	shot_down = pygame.sprite.groupcollide(bullets, twits, True, False)
	# Shoosting
	if shot_down:
		for members in shot_down.values():
			check_kills(g_settings, screen, stats, bullets, members, twits, powerups)

		# Update Score
		scores.prep_score()

	# Powah
	power_up = pygame.sprite.spritecollideany(ship, powerups)
	if power_up:
		powerups.remove(power_up)
		g_settings.ship_speed += 0.2
		ship.power_up()
	# if pickup_power:
	# 	for powers in pickup_power.values():
	# 		for power in powers:
	# 			powerups.remove(power)	
			
			
	
		

def spawn_powerup(g_settings, screen, powerups, twit):
	
	new_power = Powerup(g_settings, screen, twit)
	powerups.add(new_power)



def update_screen(g_settings, screen, ship, textbox, aliens, reticle, \
							twits, powerups, bullets, stats, scores, buttons):
	# Mouse
	global cur_scrn
	global flagged

	if not cur_scrn == stats._current_screen:
		cur_scrn = stats._current_screen
		print("cur scrn == {}".format(stats._current_screen))

	# Load background so we dont leave ship footprints everywhere
	g_settings.load_background(screen, display=stats._current_screen)
	
	if stats.game_active:
		# if _current_game is true...
		if stats._current_screen == 3:

			# Might not need this here
			global all_tweets

			# print("starting twitter mode")
			ship.update()
			twits.draw(screen)
			for bullet in bullets.sprites():
				bullet.draw_bullet()
			for power in powerups.sprites():
				power.blitme()

		scores.show_score()

	else: # Game is inactive. These are menus
		if cur_scrn == 2:
			get_infoz(g_settings, screen, twits, \
						stats, scores, reticle,textbox, buttons, \
							cur_scrn=stats._current_screen, hide=1)

		else:

			get_infoz(g_settings, screen, twits, \
					stats, scores, reticle, textbox, buttons, \
								cur_scrn=stats._current_screen)
		

	pygame.display.flip()


		# If everything breaks
	# print("LEN OF TWITS = {}".format(len(twits)))
