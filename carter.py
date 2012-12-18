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
			print "self.path=%s - self.loc=%s" % (self.path, self.loc)
			if self.path[-1][0]==self.loc.x and self.path[-1][1]==self.loc.y:
				if self.cargo:
					self.dropCargo()
				else:
					self.pickupCargo()
			else:
				self.moveAlongPath()
		elif self.cargo:
			self.dest, self.path=self.world.findDemand(self.loc, self.cargo)
		else:
			self.dest, self.path=self.world.findCargo(self.loc)

	def moveAlongPath(self):
		if self.path:
			self.loc=self.world[self.path.pop(0)]

	def dropCargo(self):
		print "DropCargo"
		pass

	def pickupCargo(self):
		print "pickupCargo"
		pass

#EOF