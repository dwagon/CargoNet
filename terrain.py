# Class definitions for terrain
import pygame
import random

import cargo

################################################################################
################################################################################
################################################################################
class MapNode(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.neighbours=set()
        self.transport=True
        self.building=None    # Reference to a building object
        self.cargo=[]
        self.image=None
        self.rect=None
                
    ############################################################################
    def turn(self):
        self.consolidateCargo()

    ############################################################################
    def consolidateCargo(self):
        if not self.cargo:
            return
        newcargo={}
        for c in self.cargo:
            if c.amount>0:
                if c.__class__ not in newcargo:
                    newcargo[c.__class__]=c.__class__()
                newcargo[c.__class__].add(c.amount)
        self.cargo=newcargo.values()

    ############################################################################
    def getCargo(self, typ=None, maxsize=9999):
        if self.building:
            c=self.building.getCargo(typ, maxsize)
            if c:
                return c
        if not typ:
            typ=random.choice(self.cargo).__class__
        for c in self.cargo[:]:
            if isinstance(c, typ):
                if c.amount<=maxsize:
                    self.cargo.remove(c)
                    return c
                else:
                    nc=typ(maxsize)
                    c.deplete(maxsize)
                    return nc
        return None

    ############################################################################
    def needs(self, cargo):
        if self.building:
            return self.building.needs(cargo)
        return None

    ############################################################################
    def dropCargo(self, cargo):
        if self.building:
            c=self.building.dropCargo(cargo)
            if c:
                return c
        self.cargo.append(cargo)
        self.consolidateCargo()

    ############################################################################
    def hasCargo(self, typ):
        for c in self.cargo:
            if typ:
                if isinstance(c,typ):
                    return True
            else:
                return True
        return False

    ############################################################################
    def addCargo(self, carg):
        self.cargo.append(carg)
        self.consolidateCargo()

    ############################################################################
    def draw(self, screen, xsize, ysize):
        if not self.rect:
            self.rect=pygame.Rect(self.x*xsize,self.y*ysize,xsize,ysize)
        screen.blit(self.image,self.rect)

    ############################################################################
    def __repr__(self):
        return "<%s:%d,%d>" % (self.__class__.__name__,self.x,self.y)

################################################################################
################################################################################
################################################################################
class Grassland(MapNode):
    def __init__(self, x, y):
        MapNode.__init__(self, x, y)
        self.transport=True
        self.image=pygame.image.load('images/grassland.png')

    ############################################################################
    def short(self):
        return 'G'

################################################################################
################################################################################
################################################################################
class Woodland(MapNode):
    def __init__(self, x, y):
        MapNode.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('images/woodland.png')

    ############################################################################
    def short(self):
        return 'W'

################################################################################
################################################################################
################################################################################
class Water(MapNode):
    def __init__(self, x, y):
        MapNode.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('images/water.png')

    ############################################################################
    def short(self):
        return '~'

################################################################################
################################################################################
################################################################################
class Mountain(MapNode):
    def __init__(self, x, y):
        MapNode.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('images/mountain.png')

    ############################################################################
    def short(self):
        return '^'

#EOF
