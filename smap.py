# Map for cargonet

import random
import sys
import os

import carter
import terrain
import astar
import building
import cargo

################################################################################
################################################################################
################################################################################
class Map(object):
    def __init__(self, height=5, width=5):
        self.nodes={}
        self.width=width
        self.height=height
        self.carters=[]
        self.buildings=[]
        self.generateMap()
        self.assignNeighbours()

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

    ############################################################################
    def addCarter(self, loc=None):
        if not loc:
            loc=self.findGrassland()
        c=carter.Carter(loc, self)
        self.carters.append(c)

    ############################################################################
    def addQuarry(self, loc=None, count=1):
        self.addBuilding(building.Quarry, self.findMountain, loc, count)

    ############################################################################
    def addLumberCamp(self, loc=None, count=1):
        self.addBuilding(building.LumberCamp, self.findWoodland, loc, count)
        
    ############################################################################
    def addBuildingSite(self, loc=None, count=1):
        self.addBuilding(building.BuildingSite, self.findGrassland, loc, count)

    ############################################################################
    def addBuilding(self, build, locfinder=None, loc=None, count=1):
        attempts=10
        if not loc and locfinder:
            loc=locfinder()
            while loc.building and attempts:
                loc=locfinder()
                attempts-=1
        if not attempts:
            print "Couldn't find room for a %s" % build.__class__.__name__
            return
        d=build(loc, self, count)
        loc.building=d
        self.buildings.append(d)

    ############################################################################
    def addStoneMason(self, loc=None, count=1):
        self.addBuilding(building.StoneMason, self.findGrassland, loc, count)

    ############################################################################
    def addCarpenter(self, loc=None, count=1):
        self.addBuilding(building.Carpenter, self.findGrassland, loc, count)

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
        for b in self.buildings:
            b.draw(screen, xsize, ysize)
        for c in self.carters:
            c.draw(screen, xsize, ysize)

    ############################################################################
    def isDemand(self, cargotype):
        """ Is there demand for this type of cargo?
        """
        for b in self.buildings:
            if b.needs(cargotype):
                return True
        return False

    ############################################################################
    def findDemand(self, loc, demandtype):
        """ Find the closest demand for demandtype
        """
        destinations=[]
        for b in self.buildings:
            if b.needs(demandtype):
                destinations.append(b.loc)
        return self.findRoute(loc, destinations)

    ############################################################################
    def getAllCargoTypes(self):
        if hasattr(self, 'allcargotypes'):
            return self.allcargotypes
        self.allcargotypes=[]
        for d in dir(cargo):
            if d[0]=='_':
                continue
            c=eval("cargo.%s" % d)
            if issubclass(c, cargo.Cargo) and c!=cargo.Cargo:
                self.allcargotypes.append(c)
        return self.allcargotypes

    ############################################################################
    def findCargo(self, loc, cargotype=[]):
        """ Find the closest cargo to loc
        """
        destinations=set()
        if not cargotype:
            cargotype=self.getAllCargoTypes()
        for ct in cargotype:
            if not self.isDemand(ct):
                print "No demand for %s" % ct
                continue
            s=set([n for n in self.nodes.values() if n.hasCargo(ct)])
            destinations=destinations.union(s)
        return self.findRoute(loc, list(destinations))

    ############################################################################
    def findRoute(self, src, destlist):
        if not destlist:
            print "No destinations specified"
            return None,[]
        if not src:
            print "No sources specified"
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
            if len(a.path) and len(a.path)<minlength:
                minlength=len(a.path)
                minroute=a.path[:]
                dest=a.target
        if not dest:
            return None,[]
        # Don't include the start point
        return dest, minroute[1:]

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
        for n in self.nodes.values():
            n.turn()
        for b in self.buildings[:]:
            b.turn()
            if b.terminate:
                b.loc.building=None
                self.buildings.remove(b)
        for c in self.carters:
            c.turn(self.carters)
        if random.randrange(100)==1:
            self.addQuarry()
            self.addLumberCamp()
        bs=len([b for b in self.buildings if isinstance(b, building.BuildingSite)])
        if not bs:
            self.addBuildingSite()

    ############################################################################
    def initialResources(self):
        self.addStoneMason()
        self.addCarpenter()
        self.addBuildingSite()
        self.addLumberCamp()
        self.addQuarry()
        self.addCarter()


#EOF
