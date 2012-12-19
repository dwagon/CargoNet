import pygame

import cargo

################################################################################
class Node(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.neighbours=set()
        self.transport=True
        self.source=None    # Reference to a source object
        self.demand=None    # Reference to a demand object
        self.cargo={}
        self.image=None
        self.rect=None
                
    ############################################################################
    def getCargo(self, typ=None, maxsize=9999):
        if not typ:
            st=self.cargo.get('stone',0)
            ti=self.cargo.get('timber',0)
            if st>ti:
                typ='stone'
            else:
                typ='timber'
        if typ=='stone':
            if self.cargo.get('stone',0)==0:
                return None
            c=cargo.Stone()
            c.amount=min(self.cargo['stone'], maxsize)
        if typ=='timber':
            if self.cargo.get('timber',0)==0:
                return None
            c=cargo.Timber()
            c.amount=min(self.cargo['timber'], maxsize)
        return c

    ############################################################################
    def dropCargo(self, cargo):
        if cargo.typ=='stone':
            self.addCargo('stone', cargo.amount)
        elif cargo.typ=='timber':
            self.addCargo('timber', cargo.amount)
        else:
            print "Unknown cargo %s" % cargo

    ############################################################################
    def hasCargo(self, typ):
        return self.cargo.get(typ,0)

    ############################################################################
    def addCargo(self, typ, amount=1):
        self.cargo[typ]=self.cargo.get(typ,0)+amount
        print "%s %s=%d" % (self, typ, self.cargo[typ])

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
        self.image=pygame.image.load('grassland.png')

    ############################################################################
    def short(self):
        return 'G'

################################################################################
class Woodland(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('woodland.png')

    ############################################################################
    def short(self):
        return 'W'

################################################################################
class Water(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('water.png')

    ############################################################################
    def short(self):
        return '~'

################################################################################
class Mountain(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y)
        self.transport=False
        self.image=pygame.image.load('mountain.png')

    ############################################################################
    def short(self):
        return '^'
