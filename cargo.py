#!/opt/local/bin/python-2.7
#
# Objects to move around in CargoNet

class Cargo(object):
    def __init__(self, smap, loc=None):
        self.smap=smap
        self.loc=loc

    def turn(self):
        pass

class Stone(Cargo):
    label='Stone'

class Timber(Cargo):
    label='Timber'
	
#EOF
