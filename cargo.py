#!/opt/local/bin/python-2.7
#
# Objects to move around in CargoNet

class Cargo(object):
    def __init__(self, smap, loc=None):
        self.dest=None
        self.smap=smap
        self.loc=loc

    def turn(self):
        if not self.dest:
            self.dest=smap.getDest(self.loc)

    def move(self, target):
        self.loc=target

#EOF
