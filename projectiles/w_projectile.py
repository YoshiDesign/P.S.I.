from pygame.sprite import Sprite

class Projectile(Sprite):
	
	def __init__(self, screen, g_settings):
		super(Projectile, self).__init__()
		
		self.bullet_width
		self.bullet_height
		
		
		
	def init_dynamic_projectile(self, color=(100,255,120), damage=1, proj=0):
		
		# Colors
		self.bullet_color = color
		self.lazer_color = color
		self.bomb_color = (244,188,66)
		
		# Damages
		self.bullet_dmg = 1
		self.lazer_dmg = 1
		self.bomb_dmg = 2
		
		
	def change_proj_dmg(self, damage=1, proj=0)
	
		if proj == 1:
			self.bullet_dmg += damage
		elif proj == 2:
			self.lazer_dmg += damage
		elif proj == 3:
			self.bomb_dmg += damage * 2
		else:
			""" This is an auxillary case """
			pass
		
