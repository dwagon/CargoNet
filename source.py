# Class detailing sources of cargo
import pygame

class Source(object):
	def __init__(self, loc, world, size):
		self.loc=loc
		self.world=world
		self.size=size
		self.image=None
		self.turn()

	def draw(self, screen, xsize, ysize):
		screen.blit(self.image, self.loc.rect)

class Quarry(Source):
	def __init__(self, loc, world, size):
		Source.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/quarry.png')

	def turn(self):
		self.loc.addCargo('stone', self.size)

class LumberCamp(Source):
	def __init__(self, loc, world, size):
		Source.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/lumbercamp.png')

	def turn(self):
		self.loc.addCargo('timber', self.size)

#EOF
