""" Data collection helpers """

class Thread_requests():

	""" Game Data to be sent to the webserver """

	def __init__(self):

		# Hash before transit, discard otherwise
		self.global_stats_dict = { 

			"power" : {
				"bulletup" : 0, 
				"lazerup" :  0,
				"bombup"  :  0,
				"speedup" :  0,
			},
			"play_info" : {
				"tw_destroy" : 0,
				"pl_destroy" : 0,
				"ship_loss" :  0,
				"win_handles": []
			},
			"score_info" : {
				"points" 	:  0,
				"high_score" : 0
			},
			"novelty" : {
				"dollars" : 0,
				"booster" : 0,
			}
		}

	@classmethod
	def listening(self, flag, enter, exit):

		""" 
			The Pipe Sentinel collecting from :
			apply_power()

		"""
		
		odds = [0,0,0]
		while True:
			print("listening")
			data = exit.recv()
			# For your health
			if data:

				"""	
					Will receive a list of 3 dicts after each game ends	
					[relay_power, relay_score, relay_other] --> globals in gf.py

				"""
				print("Collecting ... ")
				print(data)

				if data['power'] == 'bulletup':
					self.global_stats_dict['powers']['bulletup'] += 1
				if data['power'] == 'bombup':
					self.global_stats_dict['powers']['bombup'] += 1
				if data['power'] == 'lazerup':
					self.global_stats_dict['powers']['lazerup'] += 1
