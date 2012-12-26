# Class to handle things that move cargo around
import pygame

################################################################################
################################################################################
################################################################################
class Carter(object):
	def __init__(self, loc, world):
		self.loc=loc
		self.cargo=None
		self.world=world
		self.image=pygame.image.load('images/carter.png')
		self.dest, self.path=self.world.findCargo(self.loc)

    ############################################################################
	def draw(self, screen, xsize, ysize):
		screen.blit(self.image, self.loc.rect)
		self.write(screen, "cargo=%s dest=%s" % (self.cargo, self.dest), self.loc.x * xsize, self.loc.y * ysize)
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
	def turn(self):
		if self.path:
			self.moveAlongPath()
			return
		if self.cargo:
			if self.loc.needs(self.cargo):
				self.dropCargo()
				self.dest, self.path=self.world.findCargo(self.loc)
			return
		if self.loc.cargo:
			self.pickupCargo()
			self.dest, self.path=self.world.findDemand(self.loc, self.cargo)
			return
		self.dest, self.path=self.world.findCargo(self.loc)

    ############################################################################
	def moveAlongPath(self):
		self.loc=self.world[self.path.pop(0)]

    ############################################################################
	def dropCargo(self):
		print "Drop %s" % self.cargo
		self.loc.dropCargo(self.cargo)
		self.cargo=None

    ############################################################################
	def pickupCargo(self):
		self.cargo=self.loc.getCargo()
		print "Picked up %s" % self.cargo

#EOF