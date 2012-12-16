# A class that creates demand for a resource

################################################################################
class Demand(object):
	def __init__(self, loc, count=0):
		self.loc=loc
		self.required=count

	def satisfy(self, amount):
		self.required-=amount

	def satisfied(self):
		return self.required<=0

	def draw(self, screen, rect):
		pass

################################################################################
class demandsStone(Demand):
	label='Stone'

################################################################################
class demandsTimber(Demand):
	label='Timber'

#EOF