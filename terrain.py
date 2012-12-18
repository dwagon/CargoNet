import pygame

################################################################################
class Node(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.floodcount=0
        self.floodval=-999
        self.neighbours=set()
        self.transport=True
        self.image=None
        self.rect=None
                
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
