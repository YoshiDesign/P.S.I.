from pygame.sprite import Sprite
import re, os
from analyze import Analyzer

# Could probably just add this to the alien.py file

class Tweeter(Sprite):
	_tweet = []
	# Good or bad -- for debuggin'
	_total_twits = 0
	# (... sentiment=1...) infers positive by default
	def __init__(self, g_settings, screen, x, y, sentiment=1, cur_letter=""):
		Tweeter._total_twits += 1
		""" 
			Construct a letter sprite
			Must adhere to naming convention 
			e.g. "badf.bmp" "goodf.bmp"
		"""
		super(Sprite, self).__init__

		self.filepath = os.fsencode(str("sprites/characters/" + \
							str(sentiment) + str(letter) + ".bmp"))
		
		self.g_settings = g_settings
		self.sentiment = sentiment
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		print("SSS {}".format(self.sentiment))
		
		# pixel width which occurs after every last letter of every word
		self.blank_space_width = 8
		self.image = pygame.image.load(fs.decode(self.filepath))
		self.image_rect = self.image.get_rect()
		# Dimensions
		self.image_rect.y = self.image_rect.height
		self.image_rect.x = self.image_rect.width

		# For precise tracking
		#self.x = float(self.image_rect.x)

	@classmethod
	def construct_tweet_army(cls, g_settings, screen, ship, tokenized, \
											neg_words, pos_words):

		""" A closure for constructing the tweet army """

		sentiment = 1
		# tokenized = [["I", "am", "tweet!"],["I", "am", "tweet!"],["I", "am", "tweet!"]]
		# tweet = ["I", "am", "tweet!"]
		for tweet in tokenized:
			for word in tweet:
				# Eject links
				if re.search("://", word):
					continue
				if word in Analyzer._neg_words:
					sentiment = 0
				# Spaces between words
				word = str(word) + " "
				
				for letter in word:
					letter = cls(g_settings, screen, x, y, sentiment=sentiment, cur_letter=letter)
					#print(letter, end="")



	def get_col(self, g_settings):
		""" determine n(letters) in a row """
		
		# Acquire columns. Could come in handy
		self.cols = g_settings.screen_width / self.image_rect.width
		self.avail_space = self.cols - (8 * self.image_rect.width)
		return avail_space



	def get_row(self, g_settings):
		self.avail_space = g_settings.screen_height - (18 * self.image_rect.height)
		


	# def update_twit(self, g_settings, screen, ship):
	# 	self.x +=(self.g_settings.twit_speed_v *\
	# 				self.g_settings.twit_direction)
	# 	self.rect.x


	# def blitme(self, screen):
	# 	self.screen.blit(self.image, self.rect)
