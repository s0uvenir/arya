from psostructs import *
from models import *
from random import random

gbestf = Particle()
gbestp = Particle()

def pso (model, population = 100, itr = 100):
	w  = 0.3 # Inertia              0 =< w =< 1.2
	c1 = 1.8 # Cognitive Coeffcient 0 =< c1 =< 2
	c2 = 1.5 # Social Coefficient   0 =< c2 =< 2
	s = Swarm()
	m = model
	s.initialize(m, population)
	s.sort()
	gbestf = s.pop[0] #Particle with best fitness
	gbestp = s.pop[0]
	for i in range(itr):
		for particle in s.pop:
			fitness, err = particle.score()
			if fitness > particle.fitness:
				particle.fitness = fitness
				particle.pbest = particle.position
			if fitness > gbestp.fitness:
				gbestp = particle
			particle.newVelocity(w, c1, c2, gbestp, 2)
			particle.newPosition(gbestp)
	s.sort()
	return s
	

m = Schaffer()
swarm = pso(m)
for p in swarm.pop[:5]:
	print p.model + str(p.id)
	print p.position
	print p.fitness
