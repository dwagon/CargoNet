import pygame
import demand

################################################################################
class Node(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.cargo=[]
        self.demands=[]
        self.floodcount=0
        self.floodval=-999
        self.neighbours=set()
        self.transport=True
        self.image=None
                
    ############################################################################
    def draw(self, screen, xsize, ysize):
        rect=pygame.Rect(self.x*xsize,self.y*ysize,xsize,ysize)
        screen.blit(self.image,rect)
        for d in self.demands:
            d.draw(screen, rect)
        for c in self.cargo:
            c.draw(screen, rect)

    ############################################################################
    def demandStone(self, count=1):
        d=demand.demandsStone(self, count)
        self.demands.append(d)

    ############################################################################
    def demandTimber(self, count=1):
        d=demand.demandsTimber(self, count)
        self.demands.append(d)
            
    ############################################################################
    def pickDirection(self):
        """ Return all the nodes that have the highest floodval"""
        maxf=-999
        maxn=set()

        for n in self.neighbours:
            if n.floodval>maxf:
                maxf=n.floodval
        if maxf>-999:
            for n in self.neighbours:
                if n.floodval==maxf:
                    maxn.add(n)
        return maxn

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
