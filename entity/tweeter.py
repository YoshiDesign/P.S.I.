from pygame.sprite import Sprite
from collections import OrderedDict as OD
import re, os
from analyze import Analyzer


# Could probably just add this to the alien.py file

class Tweeter(Sprite):
	_tweet = []
	_tweets_read = 0
	# Good or bad -- for debuggin'
	_total_twits = 0
	# (... sentiment=1...) infers positive by default
	def __init__(self, g_settings, screen, text_data={}):
		Tweeter._total_twits += 1
		super(Sprite, self).__init__

		
		self.letter = text_data["letter"]
		self.sentiment = text_data["sentiment"]

		if isdigit(self.text_data["letter"]):
			self.filepath = os.fsencode(str("sprites/characters/" + \
								"good" + str(self.letter) + ".png"))

		elif self.text_data["sentiment"]:
			self.filepath = os.fsencode(str("sprites/characters/" + \
								"good" + str(self.letter.upper()) + ".png"))
		else:
			self.filepath = os.fsencode(str("sprites/characters/" + \
								"bad" + str(self.letter.upper()) + ".png"))

		
		
		self.g_settings = g_settings
		self.sentiment = sentiment
		self.screen = screen
		self.screen_rect = screen.get_rect()

		print("SSS {}".format(self.sentiment))
		
		# pixel width which occurs after every last letter of every word
		
		self.image = pygame.image.load(fs.decode(self.filepath))
		self.image_rect = self.image.get_rect()
		# Dimensions
		self.image_rect.y = self.image_rect.height
		self.image_rect.x = self.image_rect.width
		self.char_spacing = self.g_settings.char_spacing

		# For more granular movement
		self.x = float(self.image_rect.x)

		# For precise tracking
		#self.x = float(self.image_rect.x)

	@classmethod
	def construct_tweet_army(cls, twits, tokenized, \
								neg_words, pos_words):

		""" A closure for constructing the tweet army """
		let_num = 0
		sentiment = 1
		end_char = 0
		text_data = OD
		available_x = get_cols(self.g_settings)
		available_y = get_rows(self.g_settings)
		re_alphaNum = r"^[a-zA-Z0-9]+$"
		# I should add ! and ?

		for tweet in tokenized[:3]:

			for word in tweet:

				# Eject links & other fragments
				if re.search(re_alphaNum, word):

					if word in Analyzer._neg_words:
						sentiment = 0
					else:
						sentiment = 1

					for n, letter in enumerate(word):

						# Catch the last char in each word
						try:
							if not letter[n+1]:
								end_char = 1
						except IndexError:
							end_char = 1
							pass

						letter = letter.lower()

						# DOES LET_NUM NEED TO BE A DIGIT FOR ITERATION? I THNK SO... 

						text_data{"letter" : letter}
						text_data{"sentiment" : sentiment}
						text_data{"end_char" : end_char}
						text_data{"index no." : let_num}

						# if endchar, increase width for space

						# twit might need its own class
						# because it needs several values like sentiment and current letter
						# Unless we can pass an entire dictionary to the init function above

						character = cls(g_settings, screen, text_data=text_data)

						if text_data["end_char"]:
							width = character.image_rect.width + 5
						else:
							width = character.image_rect.width

						character.x = width + g_settings.char_spacing

						twits.add(character)


				else:
					continue
	def print_letter(self, x_pox, y_pos):
		pass

	def get_cols(self, g_settings):
		""" determine n(letters) in a row """
		
		# Acquire columns. Could come in handy
		self.cols = g_settings.screen_width / self.image_rect.width
		self.avail_space = self.cols - (8 * self.image_rect.width)
		return avail_space


	def get_rows(self, g_settings):
		self.avail_space = g_settings.screen_height - (18 * self.image_rect.height)
		

	def check_edges(self):

		screen_rect = self.screen.get_rect()
		if self.image_rect.right >= screen_rect.right:
			return True
		elif self.image_rect <= 0:
			return True

	def update(self):
		""" Movement """ 
		self.x += (self.g_settings.twit_speed *\
				self.g_settings.twit_direction)
		self.image_rect.x = self.x

	# def update_twit(self, g_settings, screen, ship):
	# 	self.x +=(self.g_settings.twit_speed_v *\
	# 				self.g_settings.twit_direction)
	# 	self.rect.x


	def blitme(self, screen):
	 	self.screen.blit(self.image, self.rect)
