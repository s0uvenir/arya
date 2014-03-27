import random
import math

class Schaffer():
	def __init__(self):
		self.name = "Schaffer"
		self.inputs = [	random.uniform(-10000, 10000) ]
		self.eqs    = [ lambda inputs: 
					math.pow(inputs[0], 2) / 10000000000,
				lambda inputs:
					(math.pow(inputs[0], 2) - 2) / 10000000000]
		
	def objectives(self):
		inlist = self.inputs[:]
		outlist = []
		for lamb in self.eqs:
			temp = lamb(inlist)
			outlist.append(temp)
		return outlist

					
					
		
#x = Schaffer()
#test = x.objectives()
#print x.inputs
#print test
