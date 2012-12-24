import pygame
import random

import cargo

################################################################################
class Node(object):
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
        if not self.cargo:
            return
        newcargo={}
        for c in self.cargo:
            if c.__class__.__name__ not in newcargo:
                newcargo[c.__class__.__name__]=c.__class__()
            newcargo[c.__class__.__name__].add(c.amount)
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
                    nc=typ()
                    nc.amount=maxsize
                    c.amount-=maxsize
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

    ############################################################################
    def hasCargo(self, typ):
        for c in self.cargo:
            if isinstance(c,typ):
                return True
        return False

    ############################################################################
    def addCargo(self, carg):
        self.cargo.append(carg)

    ############################################################################
    def loc(self):
        return self.x, self.y

    ############################################################################
    def draw(self, screen, xsize, ysize):
        if not self.rect:
            self.rect=pygame.Rect(self.x*xsize,self.y*ysize,xsize,ysize)
        screen.blit(self.image,self.rect)

    ############################################################################
    def __repr__(self):
        return "<%s:%d,%d>" % (self.__class__.__name__,self.x,self.y)

################################################################################
class Grassland(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=True
        self.image=pygame.image.load('images/grassland.png')

    ############################################################################
    def short(self):
        return 'G'

################################################################################
class Woodland(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('images/woodland.png')

    ############################################################################
    def short(self):
        return 'W'

################################################################################
class Water(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('images/water.png')

    ############################################################################
    def short(self):
        return '~'

################################################################################
class Mountain(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('images/mountain.png')

    ############################################################################
    def short(self):
        return '^'
