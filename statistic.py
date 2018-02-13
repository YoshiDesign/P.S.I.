

class Stats():
	
	def __init__(self, g_settings):
		
		self.settings = g_settings
		self.reset_stats()
		self.game_active = False
		self.score = 0
		self.high_score = 0
		
		
		
	def reset_stats(self):
		""" Revert stats to initial state """
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
		
	def game_over_net(self):
		""" Communicate to Leaderboard """
		pass
