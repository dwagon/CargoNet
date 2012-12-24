# Class for objects that create and consume cargo
import pygame

import cargo

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
	def satisfy(self, amount):
		self.required-=amount

	############################################################################
	def satisfied(self):
		return self.required<=0

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

################################################################################
class Quarry(Building):
	def __init__(self, loc, world, size):
		Building.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/quarry.png')
		self.provides=[cargo.Stone]

	############################################################################
	def turn(self):
		self.loc.addCargo(cargo.Stone(self.size))

################################################################################
class LumberCamp(Building):
	def __init__(self, loc, world, size):
		Building.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/lumbercamp.png')
		self.provides=[cargo.Timber]

	############################################################################
	def turn(self):
		self.loc.addCargo(cargo.Timber(self.size))

################################################################################
class StoneMason(Building):
	def __init__(self, loc, world, size=0):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Stone]
		self.image=pygame.image.load('images/stone_mason.png')

################################################################################
class Carpenter(Building):
	def __init__(self, loc, world, size=0):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Timber]
		self.image=pygame.image.load('images/carpenter.png')

################################################################################
class BuildingSite(Building):
	def __init__(self, loc, world, size=0):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Timber, cargo.Stone]
		self.image=pygame.image.load('images/building_site.png')

#EOF