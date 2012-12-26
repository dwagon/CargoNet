# Class to handle things that move cargo around
import pygame

################################################################################
################################################################################
################################################################################
class Carter(object):
	def __init__(self, loc, world):
		self.loc=loc
		self.size=5		# Maximum amount we can carry
		self.cargo=None
		self.world=world
		self.image=pygame.image.load('images/carter.png')
		self.dest, self.path=self.world.findCargo(self.loc)

    ############################################################################
	def draw(self, screen, xsize, ysize):
		screen.blit(self.image, self.loc.rect)
		self.write(screen, "cargo=%s" % self.cargo, self.loc.x * xsize, self.loc.y * ysize)
		if self.path:
			for n in self.path:
				red=(255,0,0)
				pygame.draw.circle(screen, red, (n[0]*xsize+xsize/2, n[1]*ysize+xsize/2), 2)

    ############################################################################
	def write(self, screen, text, x, y):
		font=pygame.font.SysFont(None, 24)
		textobj = font.render(text, 1, (0,0,0))
		textrect = textobj.get_rect()
		textrect.topleft = (x, y)
		screen.blit(textobj, textrect)

    ############################################################################
	def turn(self, allcarters):
		if self.path:
			self.moveAlongPath(allcarters)
			return
		if self.cargo:
			if self.loc.needs(self.cargo):
				self.dropCargo()
			else:
				print "Looking for demand for %s" % self.cargo
				self.dest, self.path=self.world.findDemand(self.loc, self.cargo)
			return
		if self.loc.cargo:
			for c in self.loc.cargo:
				if c.__class__ in self.loc.building.requires:
					print "Not taking %s as required by %s" % (c, self.loc.building)
					continue
				if self.world.isDemand(c):
					self.pickupCargo(c)
					self.dest, self.path=self.world.findDemand(self.loc, self.cargo)
					return
				else:
					print "No demand for %s" % c
		print "Looking for cargo to pick up"
		self.dest, self.path=self.world.findCargo(self.loc)

    ############################################################################
	def moveAlongPath(self, allcarters):
		badlocations=[c.loc for c in allcarters if c!=self]
		if self.path[0] not in badlocations:
			self.loc=self.world[self.path.pop(0)]
		else:
			print "Blocked going to %s" % self.path[0]

    ############################################################################
	def dropCargo(self):
		self.loc.dropCargo(self.cargo)
		self.cargo=None

    ############################################################################
	def pickupCargo(self, c):
		self.cargo=self.loc.getCargo(typ=c.__class__, maxsize=self.size)

#EOF