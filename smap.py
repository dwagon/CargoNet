#!/opt/local/bin/python2.7
#
# $Id$
# $HeadURL$

import random
import sys
import os

import cargo
import carter
import terrain
import astar

################################################################################
class Map(object):
    def __init__(self, height=5, width=5):
        self.nodes={}
        self.width=width
        self.height=height
        self.cargo=[]
        self.carters=[]
        self.cargotypes=['Stone', 'Timber']
        self.generateMap()
        self.assignNeighbours()

    ############################################################################
    def addCarter(self, loc):
        c=carter.Carter(loc, self)
        self.carters.append(c)

    ############################################################################
    def addCargo(self, typ, loc, count=1):
        if typ=='Stone':
            self.addStone(loc, count)
        elif typ=='Timber':
            self.addTimber(loc, count)
        else:
            Warning("Unknown Type in addCargo() %s" % typ)

    ############################################################################
    def addStone(self, loc, count=1):
        for i in range(count):
            c=cargo.Stone(self, loc)
            self.cargo.append(c)

    ############################################################################
    def addTimber(self, loc, count=1):
        for i in range(count):
            c=cargo.Timber(self, loc)
            self.cargo.append(c)

    ############################################################################
    def demandStone(self, loc, count=1):
        loc.demandStone(count)

    ############################################################################
    def demandTimber(self, loc, count=1):
        loc.demandTimber(count)

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
    def draw(self, screen, xsize, ysize):
        for n in self.nodes.values():
            n.draw(screen, xsize, ysize)
        for c in self.carters:
            c.draw(screen, xsize, ysize)

    ############################################################################
    def findDemand(self, loc, demandtype):
        """ Find the closest demand for demandtype
        """
        destinations=[]
        for n in self.nodes:
            for d in n.demands:
                if d.label==demandtype:
                    destinations.append(n.loc)
        return self.findRoute(loc, destinations)

    ############################################################################
    def findCargo(self, loc, cargotype=[]):
        """ Find the closest cargo to loc
        """
        if not cargotype:
            cargotype=self.cargotypes[:]
        destinations=[n.loc for n in self.cargo if n.label in cargotype]
        return self.findRoute(loc, destinations)

    ############################################################################
    def findRoute(self, src, destlist):
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
            if d==src:
                continue
            m=self.getRouteMap(src=src, dest=d)
            a=astar.AStar(m)
            if len(a.path)<minlength:
                minlength=len(a.path)
                minroute=a.path[:]
                dest=a.target
        return dest, minroute

    ############################################################################
    def getRouteMap(self, src, dest):
        """ Return a copy of a map suitable for route planning
        """
        routemap=""
        for x in range(self.width):
            s=""
            for y in range(self.height):
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
    def getDest(self, loc):
        """ Return the location of the demand to satisfy for a cargo 
        at location 'loc'
        """
        return None

    ############################################################################
    def turn_reset_flood(self):
        # Level the field
        for n in self.nodes.values():
            n.floodval=-999

    ############################################################################
    def turn_calcdemand(self, typ):
        # Flood out the demand
        for n in self.nodes.values():
            self.floodcount=0
            totaldemand=0
            for d in n.demands:
                if d.label==typ:
                    totaldemand+=d.required
            if totaldemand:
                self.flood(n,totaldemand)

    ############################################################################
    def satisfyDemand(self, node, typ):
        """ Go through all the cargo in this node and see if any of it
        satisfies its demands
        """
        for c in self.cargo[:]:
            if c.label!=typ:
                continue
            if c.loc!=node:
                continue
            for d in node.demands[:]:
                if d.label==typ:
                    d.satisfy(1)
                    if d.satisfied():
                        node.demands.remove(d)
                    self.cargo.remove(c)
                    break

    ############################################################################
    def turn_satisfy_neighbours(self, typ):
        # If you are next to a demand satisfy one of them
        for c in self.cargo:
            if c.label!=typ:
                continue
            # Which neighbours have a requirement that we can satisfy
            possneigh=[]
            for neigh in c.loc.neighbours:
                for d in neigh.demands:
                    if d.label==typ:
                        possneigh.append(neigh)
            if possneigh:
                target=random.choice(possneigh)
                c.move(target)
                self.satisfyDemand(target, typ)

    ############################################################################
    def turn_move_cargo(self, typ):
        # For everything that has something move it towards the demand
        moves=0
        for c in self.cargo:
            if c.label!=typ:
                continue
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
        for c in self.cargo:
            c.turn()
        for c in self.carters:
            c.turn()
        for typ in self.cargotypes:
            self.turn_reset_flood()
            self.turn_calcdemand(typ)
            self.turn_satisfy_neighbours(typ)
            moves+=self.turn_move_cargo(typ)
        return moves

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
