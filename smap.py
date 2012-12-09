#!/opt/local/bin/python2.7
#
# $Id$
# $HeadURL$

import pygame
import random
import sys
import os

################################################################################
class Node(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.amount=0
        self.tmpamount=0
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
        self.generateMap()
        self.assignNeighbours()

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
    def turn_initialise(self):
        # Level the field
        for n in self.nodes.values():
            n.floodval=-999
            n.tmpamount=n.amount

    ############################################################################
    def turn_calcdemand(self):
        # Flood out the demand
        for n in self.nodes.values():
            self.floodcount=0
            if n.demand:
                self.flood(n,n.demand)

    ############################################################################
    def turn(self):
        moves=0
        self.turn_initialise()
        self.turn_calcdemand()
        # If you are next to a demand satisfy one of them
        for n in self.nodes.values():
            if n.amount:
                nb=[x for x in n.neighbours if x.demand]
                if nb:
                    sn=random.choice(nb)
                    n.amount-=1
                    n.tmpamount-=1
                    sn.tmpamount=sn.tmpamount+1
        # For everything that has something move it towards the demand
        for n in self.nodes.values():
            if n.amount:
                possibleDirections=list(n.pickDirection())
                if not possibleDirections:
                    continue
                sn=random.choice(possibleDirections)     # If all options equal pick one at random
                if not n.amount:    # None left
                    break
                n.amount-=1
                n.tmpamount-=1
                sn.tmpamount=sn.tmpamount+1
                #sys.stderr.write("Moving from %d,%d to %d,%d\n" % (n.x,n.y, sn.x,sn.y))
                moves+=1
        # Activate the changes
        for n in self.nodes.values():
            n.amount=n.tmpamount
            if n.amount and n.demand:
                #sys.stderr.write("Satisfying demand at %s by %d\n" % (n.name,n.amount))
                n.demand-=n.amount
                n.amount=0
                if n.demand<0:
                    n.amount=-n.demand
                    n.demand=0
        return moves

################################################################################
def main():
    nl=Map(height=10,width=10)
    nl[(2,2)].amount=10
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
