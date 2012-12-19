# A class that creates demand for a resource
import pygame

################################################################################
class Demand(object):
	def __init__(self, loc, count=0):
		self.loc=loc
		self.required=count

	def satisfy(self, amount):
		self.required-=amount

	def satisfied(self):
		return self.required<=0

	def draw(self, screen, xsize, ysize):
		screen.blit(self.image, self.loc.rect)

	def needs(self, typ):
		if typ in self.requires:
			return True
		else:
			return False

	def turn(self):
		pass

################################################################################
class StoneMason(Demand):
	def __init__(self, loc, count=0):
		Demand.__init__(self, loc, count)
		self.requires=['Stone']
		self.image=pygame.image.load('images/stone_mason.png')

################################################################################
class Carpenter(Demand):
	def __init__(self, loc, count=0):
		Demand.__init__(self, loc, count)
		self.requires=['Timber']
		self.image=pygame.image.load('images/carpenter.png')

################################################################################
class BuildingSite(Demand):
	def __init__(self, loc, count=0):
		Demand.__init__(self, loc, count)
		self.requires=['Timber','Stone']
		self.image=pygame.image.load('images/building_site.png')

#EOF