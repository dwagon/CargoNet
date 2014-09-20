# Class to handle things that move cargo around
import pygame


##########################################################################
##########################################################################
class Carter(object):

    def __init__(self, loc, world):
        self.loc = loc
        self.size = 5		# Maximum amount we can carry
        self.cargo = None
        self.blockedCount = 0  # Times that we haven't been able to move
        self.terminate = False
        self.world = world
        self.image = pygame.image.load('images/carter.png')
        self.dest, self.path = self.world.findCargo(self.loc)

    ##########################################################################
    def draw(self, screen, xsize, ysize):
        screen.blit(self.image, self.loc.rect)
        self.write(screen, "cargo=%s" %
                   self.cargo, self.loc.x * xsize, self.loc.y * ysize)
        if self.path:
            for n in self.path:
                red = (255, 0, 0)
                pygame.draw.circle(
                    screen, red, (n[0] * xsize + xsize / 2, n[1] * ysize + xsize / 2), 2)

    ##########################################################################
    def write(self, screen, text, x, y):
        font = pygame.font.SysFont(None, 24)
        textobj = font.render(text, 1, (0, 0, 0))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        screen.blit(textobj, textrect)

    ##########################################################################
    def turn(self, allcarters):
        if self.path:
            self.moveAlongPath(allcarters)
            return
        if self.cargo:
            if self.loc.needs(self.cargo):
                self.dropCargo()
            else:
                if self.world.isDemand(self.cargo):
                    self.dest, self.path = self.world.findDemand(
                        self.loc, self.cargo)
                else:
                    # print "No demand for current cargo %s" % self.cargo
                    self.dropCargo()
            return
        if self.loc.cargo:
            for c in self.loc.cargo:
                # Don't take cargo from a build that requires that cargo
                if self.loc.building and c.__class__ in self.loc.building.requires:
                    continue
                if self.world.isDemand(c):
                    self.pickupCargo(c)
                    self.dest, self.path = self.world.findDemand(
                        self.loc, self.cargo)
                    return
                else:
                    pass
                    # print "No demand for %s" % c
        self.dest, self.path = self.world.findCargo(self.loc)

    ##########################################################################
    def moveAlongPath(self, allcarters):
        blocked = [(c.loc.x, c.loc.y) for c in allcarters if c != self]
        # print "path[0]=%s blocked=%s" % (self.path[0], blocked)
        if self.path[0] not in blocked:
            self.loc = self.world[self.path.pop(0)]
            self.blockedCount = 0
        else:
            self.blockedCount += 1
            for l in self.loc.neighbours:
                if (l.x, l.y) not in blocked:
                    self.loc = self.world[(l.x, l.y)]
                    break
            # Harsh, but a guaranteed logjam breaker
            if self.blockedCount == 10:
                print "Terminating self"
                self.terminate = True

    ##########################################################################
    def dropCargo(self):
        self.loc.dropCargo(self.cargo)
        self.cargo = None

    ##########################################################################
    def pickupCargo(self, c):
        self.cargo = self.loc.getCargo(typ=c.__class__, maxsize=self.size)

# EOF
