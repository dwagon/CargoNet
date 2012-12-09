#!/opt/local/bin/python2.7
#
# $Id$
# $HeadURL$

import pygame
import random
import sys
import os

import cargo

################################################################################
class Node(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.cargo=[]
        self.demand=0
        self.floodval=-999
        self.neighbours=set()
        self.transport=True
        self.image=None
                
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

################################################################################
class Map(object):
    def __init__(self, height=5, width=5):
        self.nodes={}
        self.width=width
        self.floodcount=0
        self.height=height
        self.cargo=[]
        self.generateMap()
        self.assignNeighbours()

    ############################################################################
    def addCargo(self, loc):
        c=cargo.Cargo(self, loc)
        self.cargo.append(c)

    ############################################################################
    def generateMap(self):
        altmap={}
        for x in range(self.width):
            for y in range(self.height):
                altmap[(x,y)]=random.randrange(0,100)
        altmap=self.smoothMap(altmap)
        for x in range(self.width):
            for y in range(self.height):
                if altmap[(x,y)]>70:
                    self.nodes[(x,y)]=Mountain(x,y)
                elif altmap[(x,y)]>60:
                    self.nodes[(x,y)]=Woodland(x,y)
                elif altmap[(x,y)]<35:
                    self.nodes[(x,y)]=Water(x,y)
                else:
                    self.nodes[(x,y)]=Grassland(x,y)
        
    ############################################################################
    def smoothMap(self, altmap):
        newmap={}
        for c in altmap.keys():
            s=0
            count=0
            for u in (-1,0,1):
                for v in (-1,0,1):
                    try:
                        s+=altmap[(c[0]+u,c[1]+v)]
                        count+=1
                    except KeyError:
                        pass
            newmap[c]=s/count
        return newmap
        
    ############################################################################
    def assignNeighbours(self):
        for node in self.nodes.values():
            for u in (-1,0,1):
                for v in (-1,0,1):
                    if u==0 and v==0:
                        continue
                    tmpx=node.x+u
                    tmpy=node.y+v
                    if (tmpx,tmpy) in self.nodes:
                        if self.nodes[(tmpx,tmpy)].transport:
                            node.neighbours.add(self.nodes[(tmpx,tmpy)])
        
    ############################################################################
    def __getitem__(self,key):
        return self.nodes[key]

    ############################################################################
    def flood(self, node, floodval):
        self.floodcount+=1
        node.floodval=floodval
        todo=[]
        for i in node.neighbours:
            if i.floodval<floodval-1:
                i.floodval=floodval-1
                todo.append(i)
        for i in todo:
            self.flood(i,floodval-1)

    ############################################################################
    def __repr__(self):
        out=[]
        for y in range(self.height):
            for x in range(self.width):
                out.append(self.nodes[(x,y)].short())
            out.append('\n')
        return ''.join(out)

    ############################################################################
    def getDest(self, loc):
        """ Return the location of the demand to satisfy for a cargo 
        at location 'loc'
        """
        return None

    ############################################################################
    def turn_initialise(self):
        # Level the field
        for n in self.nodes.values():
            n.floodval=-999

    ############################################################################
    def turn_calcdemand(self):
        # Flood out the demand
        for n in self.nodes.values():
            self.floodcount=0
            if n.demand:
                self.flood(n,n.demand)

    ############################################################################
    def satisfyDemand(self, node):
        numcargo=len([x for x in self.cargo if x.loc==node])
        while node.demand and numcargo:
            for c in self.cargo[:]:
                if c.loc==node:
                    node.demand-=1
                    self.cargo.remove(c)
                    numcargo-=1
                if node.demand<=0:      # Don't satisfy demand twice
                    break

    ############################################################################
    def turn_satisfy_neighbours(self):
        # If you are next to a demand satisfy one of them
        for c in self.cargo:
            nb=[x for x in c.loc.neighbours if x.demand]
            if nb:
                target=random.choice(nb)
                c.move(target)
                self.satisfyDemand(target)

    ############################################################################
    def turn_move_cargo(self):
        # For everything that has something move it towards the demand
        moves=0
        for c in self.cargo:
            possibleDirections=list(c.loc.pickDirection())
            if not possibleDirections:
                continue
            target=random.choice(possibleDirections)     # If all options equal pick one at random
            c.move(target)
            moves+=1

        return moves

    ############################################################################
    def turn(self):
        moves=0
        self.turn_initialise()
        for c in self.cargo:
            c.turn()
        self.turn_calcdemand()
        self.turn_satisfy_neighbours()
        moves+=self.turn_move_cargo()
        return moves

################################################################################
def main():
    nl=Map(height=10,width=10)
    nl[(2,2)].cargo=10
    nl[(7,7)].demand=10
    nl.flood(nl[(7,7)],10)
    for y in range(10):
        for x in range(10):
            sys.stdout.write("%04d " % nl[(x,y)].floodval)
        sys.stdout.write("\n")
    print nl.floodcount

################################################################################
if __name__=="__main__":
    main()

#EOF
