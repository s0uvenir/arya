from util import *
from structs import *
import copy
import math
import collections

def zeroR(datasetObject):
	datasetObject.update() #to be sure the headers are initialized
	for header in datasetObject.headers:
		if header.klass == True and header.numeric == False:
			pred = header.mode; 
			acc  = header.most/(float(header.n) + 0.001)
	return pred, acc
	
def NB(train, test):
	end = len(train.headers) -1
	sets = reloadDataSetByKey(train)
	count = 0.0
	for inst in test.instances:
		actual = inst.features[end].value
		results = []
		for set in sets:
			prob = 1.0
			for feature in inst.features[:-1]:	
				if feature.value == '?':
					pass
				elif set.headers[feature.id].numeric == True:
					pi = 3.1415926535
					e  = 2.7182818284
					s  = set.headers[feature.id].sd
					a  = 1/math.sqrt(2*pi*s**2)
					x  = float(feature.value)
					m  = set.headers[feature.id].mu
					b  = (x-m)**2/(2*s**2)
					answer = a*e**(-1*b)
					prob *= answer
				else:
					if set.headers[feature.id].count.has_key(feature.value) == True:
						prob *= float(set.headers[feature.id].count[feature.value])/(set.headers[end].n)
					else:
						prob *= 1/set.headers[end].n
			prob *= float(set.headers[end].n)/(train.headers[end].n + test.headers[end].n)
			results.append((prob, set.instances[0].features[end].value))
		ret = max(results)[1]
		if ret == actual:
			count +=1
	acc = count/float(len(test.instances))
	return acc
		
	
def createDT(data, attributes, target, fitness):
	#Creates a decision tree using a dataSet object
	data = data[:]
	
	#print data
	vals = [record[target] for record in data]
	default = most(data)	
	#If empty or no attributes
	if not data or (len(attributes) -1) <= 0:
		return default
	#if all cases have the same class
	elif vals.count(vals[0]) == len(vals):
		return vals[0]
	else:
		#choose next best split criteria (infogain)
		best = nextBestAttr(data, attributes, target, fitness)
		#create new decision tree
		tree = {best:collections.defaultdict(lambda: default)}
	
		#fill in nodes
		vals = getValues(data, best)
		for val in vals:
			subtree = createDT(getExamples(data, best, val),
					[attr for attr in attributes if attr != best],
					target, fitness)
			#add subtree to new tree
			tree[best][val] = subtree
	return tree
		
		
#ds = loadDataSet(dataSetList[0], "all")
#createDT(train, 

