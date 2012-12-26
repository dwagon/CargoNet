# Class for objects that create and consume cargo
import pygame
import random

import cargo

################################################################################
################################################################################
################################################################################
class Building(object):
	def __init__(self, loc, world, size):
		self.loc=loc
		self.world=world
		self.size=size
		self.image=None
		self.requires=[]
		self.provides=[]

	############################################################################
	def draw(self, screen, xsize, ysize):
		screen.blit(self.image, self.loc.rect)

	############################################################################
	def turn(self):
		pass

	############################################################################
	def dropCargo(self, carg):
		""" Notification that cargo has been dropped here"""
		return None

	############################################################################
	def getCargo(self, typ, amount):
		""" Notification that cargo has been picked up from here"""
		return None

	############################################################################
	def needs(self, carg):
		for t in self.requires:
			if isinstance(carg,t):
				return True
		return False

	############################################################################
	def drawText(self, text, screen, xsize, ysize):
		font = pygame.font.SysFont(None, 20)
		textobj = font.render(text, 1, (50,50,50))
		textrect = textobj.get_rect()
		textrect.topleft = (self.loc.x * xsize, self.loc.y * ysize)
		screen.blit(textobj, textrect)

################################################################################
################################################################################
################################################################################
class Quarry(Building):
	def __init__(self, loc, world, size):
		Building.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/quarry.png')
		self.provides=[cargo.Stone]
		self.capacity=20

	############################################################################
	def draw(self, screen, xsize, ysize):
		Building.draw(self, screen, xsize, ysize)
		self.drawText("%d" % self.capacity, screen, xsize, ysize)

	############################################################################
	def turn(self):
		for c in self.loc.cargo:
			if isinstance(c,cargo.Stone):
				if c.amount>=5:
					return
		make=min(self.size, self.capacity)
		self.capacity-=make
		if self.capacity<=0:
			self.provides=[]
		else:
			self.loc.addCargo(cargo.Stone(make))

################################################################################
################################################################################
################################################################################
class LumberCamp(Building):
	def __init__(self, loc, world, size):
		Building.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/lumbercamp.png')
		self.provides=[cargo.Wood]
		self.capacity=20

	############################################################################
	def draw(self, screen, xsize, ysize):
		Building.draw(self, screen, xsize, ysize)
		self.drawText("%d" % self.capacity, screen, xsize, ysize)

	############################################################################
	def turn(self):
		for c in self.loc.cargo:
			if isinstance(c,cargo.Wood):
				if c.amount>=5:
					return
		make=min(self.size, self.capacity)
		self.capacity-=make
		if self.capacity<=0:
			self.provides=[]
		else:
			self.loc.addCargo(cargo.Wood(make))

################################################################################
################################################################################
################################################################################
class StoneMason(Building):
	def __init__(self, loc, world, size=1):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Stone]
		self.image=pygame.image.load('images/stone_mason.png')

	############################################################################
	def turn(self):
		for c in self.loc.cargo:
			if isinstance(c,cargo.Stone):
				c.deplete(self.size)
		print "SM: %s" % self.loc.cargo

################################################################################
################################################################################
################################################################################
class Carpenter(Building):
	""" Building that consumes wood and converts it into timber
	"""
	def __init__(self, loc, world, size=1):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Wood]
		self.provides=[cargo.Timber]
		self.image=pygame.image.load('images/carpenter.png')

	############################################################################
	def turn(self):
		for c in self.loc.cargo:
			if isinstance(c,cargo.Wood):
				amt=min(self.size, c.amount)
				c.deplete(amt)
				self.loc.addCargo(cargo.Timber(amt))
		print "C: %s" % self.loc.cargo

################################################################################
################################################################################
################################################################################
class BuildingSite(Building):
	def __init__(self, loc, world, size=1):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Timber, cargo.Stone]
		self.image=pygame.image.load('images/building_site.png')

	############################################################################
	def turn(self):
		if self.loc.cargo:
			c=random.choice(self.loc.cargo)
			amt=min(self.size, c.amount)
			c.deplete(amt)
		print "BS: %s" % self.loc.cargo

#EOF