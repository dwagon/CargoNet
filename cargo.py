#!/opt/local/bin/python-2.7
#
# Objects to move around in CargoNet

class Cargo(object):
    def __init__(self):
        self.typ=None
        self.amount=0

    def turn(self):
        pass

class Stone(Cargo):
    def __init__(self):
        Cargo.__init__(self)
        self.typ='stone'
	
class Timber(Cargo):
    def __init__(self):
        Cargo.__init__(self)
        self.typ='timber'
#EOF
