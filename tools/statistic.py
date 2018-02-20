import pygame
from analyze import Analyzer

class Stats():
	
	# 0 = reg || 1 = twitter
	_current_game = 0

	def __init__(self, g_settings):
		
		self.g_settings = g_settings
		self.reset_all()
		# Game States
		self.game_active = False
		self.play_active = False
		self.twit_active = False
		# Statistics
		self.score = 0
		self.high_score = 0
		
	@staticmethod
	def switch_game():
		""" 
			THIS IS AN ENDPOINT for post sentiment analysis checks
			@staticmethod required
		"""
		if Stats._current_game == 0:
			Stats._current_game = 1
		else:
			Stats._current_game = 0
	
		
		

	def start_game(self, game=""):

		self.game_active = True
		
		self.g_settings.init_dynamic_settings()

		pygame.mouse.set_visible(False)

		if game == "tw":
			# Change to a twitter game
			print("ENGAGE TWITTER")
			Stats.switch_game()

	def reset_all(self):
		""" Revert stats to initial state """
		self.ships_left = self.g_settings.ship_limit
		self.score = 0
		self.level = 1
		
	def game_over_net(self):
		""" Communicate to Leaderboard """
		pass
