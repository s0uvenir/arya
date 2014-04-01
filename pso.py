from psostructs import *
from models import *

gbestf = Particle()
gbestp = Particle()

def pso (model, population = 10, itr = 10):
	w  = 0.3 # Inertia              0 =< w =< 1.2
	c1 = 2.1 # Cognitive Coeffcient 0 =< c1 =< 2
	c2 = 1.3 # Social Coefficient   0 =< c2 =< 2
	s = Swarm()
	m = model
	s.initialize(m, population)
	s.sort()
	gbestf = s.pop[0] #Particle with best fitness
	gbestp = s.pop[0]
	for i in range(itr):
		gbestf = s.pop[0] #Particle with best fitness
		gbestp = s.pop[0]
		for particle in s.pop:
			if particle != gbestp:
				particle.newVelocity(w, c1, c2, gbestp, 1)
				particle.newPosition(gbestp, gbestf)
				particle.score()
	s.sort()
	return s
	

m = Schaffer()
swarm = pso(m)
for s in swarm.pop:
	print s.position
	print s.velocity
	print s.fitness
