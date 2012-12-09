#!/opt/local/bin/python2.7
#
# $Id$
# $HeadURL$

import random
import sys
import os

################################################################################
class Node(object):
    def __init__(self, name=''):
        self.name=name
        self.amount=0
        self.tmpamount=0
        self.demand=0
        self.floodval=-9999
        self.neighbours=set()

    ############################################################################
    def pickDirection(self):
        """ Return all the nodes that have the highest floodval"""
        maxf=0
        maxn=set()

        for n in self.neighbours:
            if n.floodval>maxf:
                maxf=n.floodval
        if maxf:
            for n in self.neighbours:
                if n.floodval==maxf:
                    maxn.add(n)
        return maxn

    ############################################################################
    def __repr__(self):
        return "<Node: %s: %s>" % (self.name, ",".join([n.name for n in self.neighbours]))

################################################################################
class NodeList(object):
    def __init__(self, numnodes=5):
        names=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.nodes=[]
        for i in range(numnodes):
            self.nodes.append(Node(names[i%len(names)]))
        connected=False
        while not connected:
            self.entangle()
            connected=self.check_connectivity()

    ############################################################################
    def __getitem__(self,key):
        return self.nodes[key]

    ############################################################################
    def check_connectivity(self):
        for i in self.nodes:
            i.connected=False
        self.check_node_connectivity(self.nodes[0])
        connected=True
        for i in self.nodes:
            if not i.connected:
                connected=False
                break
        return connected

    ############################################################################
    def check_node_connectivity(self, node):
        if node.connected:
            return
        node.connected=True
        for i in node.neighbours:
            self.check_node_connectivity(i)

    ############################################################################
    def flood(self, node, floodval):
        if node.floodval<floodval:
            node.floodval=floodval
            for i in node.neighbours:
                self.flood(i,floodval-1)
        
    ############################################################################
    def entangle(self):
        for i in self.nodes:
            if len(i.neighbours)<3:
                count=100
                while count:
                    count-=1
                    rn=random.choice(self.nodes)
                    if rn==i:
                        continue
                    num=len(rn.neighbours)
                    if num<3:
                        rn.neighbours.add(i)
                        i.neighbours.add(rn)
                        count=0

    ############################################################################
    def dot(self, fd):
        fd.write("digraph G {\n")
        drawn=set()
        for i in self.nodes:
            fd.write('%s [shape=box,' % i.name)
            fd.write('label="%s\\n%d -> %d (%d)"' % (i.name, i.amount, i.demand, i.floodval))
            if i.demand:
                fd.write(',color=blue%d,style=filled' % (1+i.demand/5))
            if i.amount:
                fd.write(',color=red%d,style=filled' % (1+i.amount/5))
            fd.write('];\n')
            for n in i.neighbours:
                if (n,i) not in drawn:
                    fd.write("%s -> %s [dir=both];\n" % (i.name, n.name))
                    drawn.add((n,i))
                    drawn.add((i,n))
        fd.write("}\n")

    ############################################################################
    def __repr__(self):
        s=""
        for node in self.nodes:
            s+="%s\n" % `node`
        return s

    ############################################################################
    def turn(self):
        moves=0
        for n in self.nodes:
            n.floodval=-9999
            n.tmpamount=n.amount
        for n in self.nodes:
            if n.demand:
                self.flood(n,n.demand)
        for n in self.nodes:
            if n.amount:
                for sn in n.pickDirection():
                    if not n.amount:
                        break
                    n.amount-=1
                    n.tmpamount-=1
                    sn.tmpamount=sn.tmpamount+1
                    #sys.stderr.write("Moving from %s to %s\n" % (n.name, sn.name))
                    moves+=1
        for n in self.nodes:
            n.amount=n.tmpamount
            if n.amount and n.demand:
                #sys.stderr.write("Satisfying demand at %s by %d\n" % (n.name,n.amount))
                n.demand-=n.amount
                n.amount=0
        return moves

################################################################################
def main():
    numnodes=15
    nl=NodeList(numnodes)
    nl[0].amount=19
    nl[1].amount=19
    nl[-4].demand=10
    nl[-3].demand=10
    nl[-2].demand=3
    nl[-1].demand=7

    for t in range(1000):
        sys.stderr.write("Turn %d\n" % t)
        f=os.popen('dot -Tpng -o map%02d.png' % t, 'w')
        moves=nl.turn()
        nl.dot(f)
        f.close()
        if not moves:
            break

################################################################################
if __name__=="__main__":
    main()

#EOF
