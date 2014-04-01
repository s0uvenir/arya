import random
import math

class Schaffer():
	def __init__(self):
		self.name = "Schaffer"
		self.x1 = random.uniform(-10, 10)
		self.inputs = [	self.x1 ]
		self.outputs = []
		self.eqs    = [ lambda inputs: 
					math.pow(inputs[0], 2),
				lambda inputs:
					(math.pow(inputs[0], 2) - 2)]
		
	def objectives(self):
		inlist = self.inputs[:]
		outlist = []
		for lamb in self.eqs:
			temp = lamb(inlist)
			outlist.append(temp)
		self.outputs = outlist

							
		
#x = Schaffer()
#x.inputs[0] = 10
#test = x.objectives()
#print x.inputs
#print test
