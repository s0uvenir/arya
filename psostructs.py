import random
import math
from math import sin, sqrt

class Particle():
	def __init__(self):
		self.model = ""
		self.id = 0
		self.positon = []
		self.pbest = []
		self.velocity = []
		self.fitness = 0

	def newVelocity(self, w, c1, c2, gbestp, dimension):
		c3 = c1+c2
		k = 2/(abs(2-c3-math.sqrt(c3*c3)-(4*c3)))
		for i in range(len(self.position)):
			b = self.pbest[i]
			p = self.position[i]
			g = gbestp.position[i]
			r1 = random.uniform(b, p)
			r2 = random.uniform(g, p)
			v = self.velocity[i]
			v = k*(w*v+c1*r1+c2*r2)
			self.velocity[i] = v

	def newPosition(self, gbestp):
		if self != gbestp:
			for i in range(len(self.position)):
				self.position[i] += self.velocity[i]

	def score(self): #f6
		para = self.position*10
		para = self.position[0:2]
		num = (sin(sqrt((para[0] * para[0]) + (para[1] * para[1])))) * \
        	      (sin(sqrt((para[0] * para[0]) + (para[1] * para[1])))) - 0.5
		denom = (1.0 + 0.001 * ((para[0] * para[0]) + (para[1] * para[1]))) * \
		        (1.0 + 0.001 * ((para[0] * para[0]) + (para[1] * para[1])))
    		f6 =  0.5 - (num/denom)
    		errorf6 = 1 - f6
		#self.fitness = f6
    		return f6, errorf6
		
class Swarm():
	def __init__(self):
		self.pop = []
	def initialize(self, model, population = 10):
		for i in range(population):
			p = Particle()
			model.objectives()
			p.id = i
			p.model = model.name
			p.position = model.outputs
			p.pbest = model.outputs
			p.velocity = [0]*(len(p.position))
			p.score()
			self.pop.append(p)
	def sort(self):
		self.pop.sort(key = lambda x: x.fitness, reverse = True)
			



