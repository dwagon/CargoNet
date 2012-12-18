#!/opt/local/bin/python2.7
# Map for cargonet

import random
import sys
import os

import cargo
import carter
import demand
import terrain
import astar
import source

################################################################################
class Map(object):
    def __init__(self, height=5, width=5):
        self.nodes={}
        self.width=width
        self.height=height
        self.cargo=[]
        self.carters=[]
        self.demands=[]
        self.sources=[]
        self.cargotypes=['Stone', 'Timber']
        self.generateMap()
        self.assignNeighbours()

    ############################################################################
    def addCarter(self, loc=None):
        if not loc:
            loc=self.findGrassland()
        c=carter.Carter(loc, self)
        self.carters.append(c)

    ############################################################################
    def addQuarry(self, loc=None, count=1):
        if not loc:
            loc=self.findMountain()
        s=source.Quarry(loc, self, count)
        self.sources.append(s)

    ############################################################################
    def addLumberCamp(self, loc=None, count=1):
        if not loc:
            loc=self.findWoodland()
        s=source.LumberCamp(loc, self, count)
        self.sources.append(s)
        
    ############################################################################
    def addBuildingSite(self, loc=None, count=1):
        if not loc:
            loc=self.findGrassland()
        d=demand.BuildingSite(loc, count)
        self.demands.append(d)

    ############################################################################
    def addStoneMason(self, loc=None, count=1):
        if not loc:
            loc=self.findGrassland()
        d=demand.StoneMason(loc, count)
        self.demands.append(d)

    ############################################################################
    def addStone(self, loc):
        self.cargo.append(cargo.Stone(self, loc))

    ############################################################################
    def addTimber(self, loc):
        self.cargo.append(cargo.Timber(self, loc))

    ############################################################################
    def addCarpenter(self, loc=None, count=1):
        if not loc:
            loc=self.findGrassland()
        d=demand.Carpenter(loc, count)
        self.demands.append(d)

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
                    self.nodes[(x,y)]=terrain.Mountain(x,y)
                elif altmap[(x,y)]>60:
                    self.nodes[(x,y)]=terrain.Woodland(x,y)
                elif altmap[(x,y)]<35:
                    self.nodes[(x,y)]=terrain.Water(x,y)
                else:
                    self.nodes[(x,y)]=terrain.Grassland(x,y)

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
        """ Create a list of all neighbouring squares that are transportable to
        """
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
    def __repr__(self):
        out=[]
        for y in range(self.height):
            for x in range(self.width):
                out.append(self.nodes[(x,y)].short())
            out.append('\n')
        return ''.join(out)

    ############################################################################
    def draw(self, screen, xsize, ysize):
        for n in self.nodes.values():
            n.draw(screen, xsize, ysize)
        for d in self.demands:
            d.draw(screen, xsize, ysize)
        for s in self.sources:
            s.draw(screen, xsize, ysize)
        for c in self.carters:
            c.draw(screen, xsize, ysize)

    ############################################################################
    def findDemand(self, loc, demandtype):
        """ Find the closest demand for demandtype
        """
        print "findDemand(loc=%s, demandtype=%s)" % (loc, demandtype)
        destinations=[]
        for d in self.demands:
            if d.needs(demandtype):
                destinations.append(d.loc)
        return self.findRoute(loc, destinations)

    ############################################################################
    def findCargo(self, loc, cargotype=[]):
        """ Find the closest cargo to loc
        """
        if not cargotype:
            cargotype=self.cargotypes[:]
        destinations=list(set([n.loc for n in self.cargo if n.label in cargotype]))
        print "Looking at %s for %s" % (destinations, ",".join(cargotype))
        return self.findRoute(loc, destinations)

    ############################################################################
    def findRoute(self, src, destlist):
        #print src
        if not destlist:
            Warning("No destinations specified")
            return None,[]
        if not src:
            Warning("No sources specified")
            return None,[]
        minlength=999
        minroute=None
        dest=None
        for d in destlist:
            if d==src:  # Cant route to own location
                continue
            m=self.getRouteMap(src=src, dest=d)
            a=astar.AStar(m)
            for i in a.step():  # Need to fix path so it doesn't do step wise
                pass
            if len(a.path)<minlength:
                minlength=len(a.path)
                minroute=a.path[:]
                dest=a.target
        #print "dest=%s, minroute=%s" % (dest, minroute)
        return dest, minroute

    ############################################################################
    def getRouteMap(self, src, dest):
        """ Return a copy of a map suitable for route planning
        """
        routemap=""
        for y in range(self.height):
            s=""
            for x in range(self.width):
                if x==src.x and y==src.y:
                    s+=astar.SOURCE
                elif x==dest.x and y==dest.y:
                    s+=astar.TARGET
                else:
                    if self.nodes[(x,y)].transport:
                        s+=astar.UNBLOCKED
                    else:
                        s+=astar.BLOCKED
            routemap+="%s\n" % s
        return routemap

    ############################################################################
    def turn(self):
        for s in self.sources:
            s.turn()
        for d in self.demands:
            d.turn()
        for c in self.cargo:
            c.turn()
        for c in self.carters:
            c.turn()

    ############################################################################
    def findGrassland(self):
        return self.findType('Grassland')

    ############################################################################
    def findWoodland(self):
        return self.findType('Woodland')

    ############################################################################
    def findMountain(self):
        return self.findType('Mountain')

    ############################################################################
    def findType(self, typ):
        nodelist=self.nodes.values()
        random.shuffle(nodelist)
        for n in nodelist:
            if n.__class__.__name__==typ:
                if n.neighbours:
                    return n
        sys.stderr.write("Couldn't find any %s\n" % typ)
        return None

#EOF
