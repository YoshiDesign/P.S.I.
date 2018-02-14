import pygame
import os
from pygame.locals import *


class Spritesheet:

	def __init__(self, fp, cols, rows, index=0):
		
		self.sheet = pygame.image.load(os.fsdecode(fp)).convert_alpha()
		
		self.cols = cols
		self.rows = rows
		self.totalCells = self.cols * self.rows
		
		self.rect = self.sheet.get_rect()
		# Width of individual sprite
		w = self.cellWidth = self.rect.width / cols
		# Height of individual sprite
		h = self.cellHeight = self.rect.height / rows
		# Half the width and half the height of each CELL
		hw, hh = self.cellCenter = (w/2, h/2)
		print(w, h)
		
		# A list of cells (a list of rectangles repr. each cell in the spritesheet)
		self.cells = list([(i % cols * w, index / cols * h, w, h) for i in range(self.totalCells)])
		# Offsets
		print(self.cells)
		self.handle = list([
		(0,0), (-hw,0), (-w,0),
		(0, -hh), (-hw, -hh), (-w, -hh),
		(0, -h), (-hw, -h), (-w, -h),])
		
	def blitme(self, surface, cellindex, x, y, handle=0):
		# Cuts out our selected sprite
		surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellindex])
		
