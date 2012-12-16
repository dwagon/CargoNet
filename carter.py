# Class to handle things that move cargo around
import pygame

class Carter(object):
	def __init__(self, loc, world):
		self.loc=loc
		self.cargo=None
		self.dest=None
		self.world=world
		self.path=[]
		self.image=pygame.image.load('carter.png')

	def draw(self, screen, xsize, ysize):
		rect=pygame.Rect(self.loc.x*xsize, self.loc.y*ysize, xsize, ysize)
		screen.blit(self.image, rect)

	def turn(self):
		if not self.cargo:
			self.dest, self.path=self.world.findCargo(self.loc)
		else:
			self.dest, self.path=self.world.findDemand(self.loc, self.cargo)
		self.moveTowards(self.dest)

	def moveTowards(self, loc):
		pass

#EOF