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
		self.terminate=False

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
			if carg==t or isinstance(carg,t):
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
		numstone=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Stone)])
		self.drawText("%d - %d" % (self.capacity, numstone), screen, xsize, ysize)

	############################################################################
	def turn(self):
		for c in self.loc.cargo:
			if isinstance(c,cargo.Stone):
				if c.amount>=5:
					return
		amt=min(self.size, self.capacity)
		self.capacity-=amt
		if self.capacity<=0:
			self.provides=[]
			if not self.loc.cargo:
				self.terminate=True
		else:
			self.loc.addCargo(cargo.Stone(amt))

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
		numwood=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Wood)])
		self.drawText("%d - %d" % (self.capacity, numwood), screen, xsize, ysize)

	############################################################################
	def turn(self):
		for c in self.loc.cargo:
			if isinstance(c,cargo.Wood):
				if c.amount>=5:
					return
		amt=min(self.size, self.capacity)
		self.capacity-=amt
		if self.capacity<=0:
			self.provides=[]
			if not self.loc.cargo:
				self.terminate=True
		else:
			self.loc.addCargo(cargo.Wood(amt))

################################################################################
################################################################################
################################################################################
class StoneMason(Building):
	def __init__(self, loc, world, size=1, rate=5):
		Building.__init__(self, loc, world, size)
		self.rate=rate
		self.requires=[cargo.Stone]
		self.provides=[cargo.Blocks]
		self.image=pygame.image.load('images/stone_mason.png')
		self.turncount=0

	############################################################################
	def turn(self):
		self.turncount+=1
		if self.turncount%self.rate==0:
			for c in self.loc.cargo:
				if isinstance(c,cargo.Stone):
					amt=min(self.size, c.amount)
					c.deplete(amt)
					self.loc.addCargo(cargo.Blocks(amt))
		# Shutdown if we have surplus production
		numblocks=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Blocks)])
		if numblocks>20:
			self.requires=[]
		else:
			self.requires=[cargo.Stone]

	############################################################################
	def draw(self, screen, xsize, ysize):
		Building.draw(self, screen, xsize, ysize)
		numstone=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Stone)])
		numblocks=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Blocks)])
		self.drawText("%d - %d" % (numstone, numblocks), screen, xsize, ysize)

################################################################################
################################################################################
################################################################################
class Carpenter(Building):
	""" Building that consumes wood and converts it into timber
	"""
	def __init__(self, loc, world, size=1, rate=2):
		Building.__init__(self, loc, world, size)
		self.rate=rate
		self.requires=[cargo.Wood]
		self.provides=[cargo.Timber]
		self.image=pygame.image.load('images/carpenter.png')
		self.turncount=0

	############################################################################
	def turn(self):
		self.turncount+=1
		if self.turncount%self.rate==0:
			for c in self.loc.cargo:
				if isinstance(c,cargo.Wood):
					amt=min(self.size, c.amount)
					c.deplete(amt)
					self.loc.addCargo(cargo.Timber(amt))
		# Shutdown if we have surplus production
		numtimber=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Timber)])
		if numtimber>20:
			self.requires=[]
		else:
			self.requires=[cargo.Wood]

	############################################################################
	def draw(self, screen, xsize, ysize):
		Building.draw(self, screen, xsize, ysize)
		numwood=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Wood)])
		numtimber=sum([c.amount for c in self.loc.cargo if isinstance(c, cargo.Timber)])
		self.drawText("%d - %d" % (numwood, numtimber), screen, xsize, ysize)

################################################################################
################################################################################
################################################################################
class BuildingSite(Building):
	def __init__(self, loc, world, size=1):
		Building.__init__(self, loc, world, size)
		self.requires=[cargo.Timber, cargo.Blocks]
		self.image=pygame.image.load('images/building_site.png')
		self.amounts={cargo.Timber: 8, cargo.Blocks: 8}
		if random.randrange(10)==1:
			self.becomes=Carpenter
		elif random.randrange(10)==1:
			self.becomes=StoneMason
		else:
			self.becomes=House

	############################################################################
	def turn(self):
		if self.loc.cargo:
			c=random.choice(self.loc.cargo)
			amt=min(self.size, c.amount, self.amounts[c.__class__])
			self.amounts[c.__class__]-=amt
			if self.amounts[c.__class__]<=0:
				if c.__class__ in self.requires:
					self.requires.remove(c.__class__)
			c.deplete(amt)
		if sum(self.amounts.values())==0:
			self.world.addBuilding(self.becomes, loc=self.loc)
			self.terminate=True

	############################################################################
	def draw(self, screen, xsize, ysize):
		Building.draw(self, screen, xsize, ysize)
		numtimber=self.amounts.get(cargo.Timber,0)
		numblocks=self.amounts.get(cargo.Blocks,0)
		self.drawText("T%d - B%d" % (numtimber, numblocks), screen, xsize, ysize)

################################################################################
################################################################################
################################################################################
class House(Building):
	def __init__(self, loc, world, size=1):
		Building.__init__(self, loc, world, size)
		self.image=pygame.image.load('images/house.png')
		self.world.addCarter()

#EOF