#!/opt/local/bin/python-2.7
#
# Objects to move around in CargoNet

###############################################################################
class Cargo(object):
    def __init__(self, size=0):
        self.name=None
        self.amount=size

    ###########################################################################
    def turn(self):
        pass

    ###########################################################################
    def add(self, amt):
        self.amount+=amt

    ###########################################################################
    def __repr__(self):
        return "%s x %d" % (self.name, self.amount)

###############################################################################
class Stone(Cargo):
    def __init__(self, size=0):
        Cargo.__init__(self, size)
        self.name='stone'
	
###############################################################################
class Timber(Cargo):
    def __init__(self, size=0):
        Cargo.__init__(self, size)
        self.name='timber'
#EOF
