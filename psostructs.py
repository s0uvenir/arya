import random
import math

class Particle():
	def __init__(self):
		self.positon = []
		self.pbest = []
		self.velocity = 0.01
		self.fitness = 0
	def newVelocity(self, w, c1, c2, gbestp, dimension):
		r1 = random.uniform(0.0, 1.0) 
		r2 = random.uniform(0.0, 1.0) #same
		new = (w * self.velocity) + ((c1 * r1) * (self.pbest[dimension - 1] - self.position[dimension -1]))
		+ ((c2 * r2) * (gbestp.position[dimension - 1] - self.position[dimension -1]))
		self.velocity = new
	def newPosition(self, gbestp, gbestf):
		if self != gbestf:
			for i in range(len(self.position)):
				num1 = i
				num2 = gbestp.position[i]
				num3 = self.position[i]
				velocity = self.velocity
				self.position[i] = velocity * (num1 - num2)
	def score(self):
		nums = map(lambda x: math.pow(x, 2), self.position[:])
		fitness = 0
		for i in nums:
			fitness += i
		self.fitness = math.sqrt(fitness)
		
				

class Swarm():
	def __init__(self):
		self.pop = []
	def initialize(self, model, population = 10):
		for i in range(population):
			p = Particle()
			model.objectives()
			p.position = model.outputs
			p.pbest = model.inputs
			p.score()
			self.pop.append(p)
	def sort(self):
		self.pop.sort(key = lambda x: x.fitness, reverse = True)
			



