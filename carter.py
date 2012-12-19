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
		screen.blit(self.image, self.loc.rect)
		if self.path:
			for n in self.path:
				red=(255,0,0)
				pygame.draw.circle(screen, red, (n[0]*xsize+xsize/2, n[1]*ysize+xsize/2), 2)

	def turn(self):
		if self.path:
			self.moveAlongPath()
		if not self.path:
			if self.cargo:
				self.dropCargo()
				self.dest, self.path=self.world.findCargo(self.loc)
			else:
				self.pickupCargo()
				self.dest, self.path=self.world.findDemand(self.loc, self.cargo)

	def moveAlongPath(self):
		self.loc=self.world[self.path.pop(0)]

	def dropCargo(self):
		self.loc.dropCargo(self.cargo)

	def pickupCargo(self):
		self.cargo=self.loc.getCargo()

#EOF