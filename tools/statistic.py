import pygame
from analyze import Analyzer

class Stats():
	
	# 0 = menu 1 = twitter
	_current_screen = 0

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
	def menu_mode():
		""" 
			Game mode sanity check
			A good endpoint for post analysis results before game begins
		"""
		if Stats._current_screen:
			Stats._current_screen = 0
		else:
			Stats._current_screen = 0

		return True
			
	@staticmethod
	def twit_mode():
		if Stats._current_screen == 0:
			Stats._current_screen = 3
		else:
			Stats._current_screen = 3

		return True

	@staticmethod
	def login_mode():
		if Stats._current_screen == 0 or Stats._current_screen:
			Stats._current_screen = 1
		else:
			Stats._current_screen = 0

		return True

	@staticmethod
	def pass_mode():
		if Stats._current_screen == 1:
			Stats._current_screen = 2
		else:
			Stats._current_screen = 2
		return True

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
