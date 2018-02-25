import pygame
from analyze import Analyzer

class Stats():
	
	# 0 = reg || 1 = twitter
	_current_game = 0

	def __init__(self, g_settings):
		
		self.g_settings = g_settings
		# Game States
		self.game_active = False
		# self.end_game = False

		# Statistics
		self.score = 0
		self.high_score = 0
		self.level = 1

		self.reset_all()
		
	@staticmethod
	def base_mode():
		""" 
			Game mode sanity check
			A good endpoint for post analysis results before game begins
		"""
		if Stats._current_game == 1:
			Stats._current_game = 0
		else:
			Stats._current_game = 0
			
	@staticmethod
	def twit_mode():
		if Stats._current_game == 0:
			Stats._current_game = 1
		else:
			Stats._current_game = 1
	
	def update_tweets(self):
		pass
			
	def reset_all(self):
		""" Revert stats to initial state """
		self.ships_left = self.g_settings.ship_limit
		self.score = 0
		self.level = 1
		# finally
		self.g_settings.init_dynamic_settings()
		
	def game_over_net(self):
		""" Communicate to Leaderboard """
		pass
