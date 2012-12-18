# Class detailing sources of cargo
import pygame

class Source(object):
	def __init__(self, loc, world, size):
		self.loc=loc
		self.world=world
		self.size=size
		self.image=None

	def draw(self, screen, xsize, ysize):
		screen.blit(self.image, self.loc.rect)

	def turn(self):
		pass

class Quarry(Source):
	def __init__(self, loc, world, size):
		Source.__init__(self, loc, world, size)
		self.image=pygame.image.load('quarry.png')

	def turn(self):
		for i in range(self.size):
			self.world.addStone(self.loc)

class LumberCamp(Source):
	def __init__(self, loc, world, size):
		Source.__init__(self, loc, world, size)
		self.image=pygame.image.load('lumbercamp.png')

	def turn(self):
		for i in range(self.size):
			self.world.addTimber(self.loc)

#EOF
