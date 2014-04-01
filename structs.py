#Structures
from random import shuffle as shuffle
import math
import copy



class DataSet:
	def __init__(self):
		self.name	= ""
		self.headers  	= []
		self.instances 	= []
		self.summary	= ""
		self.klassLoc   = 0
	def split(self, n):	
		instances = self.instances
		shuffle(instances)
		if n == 0:
			trainDataSet	= self.copy()
			
			testDataSet 	= self.copy()
			
			return trainDataSet, testDataSet
		else:

			b = len(instances)/n
			test = []
			train = []	

			trainDataSet	= self.copy()
			trainDataSet.instances = []
			testDataSet 	= self.copy()
			testDataSet.instances = []

			test = instances[:b]
			train = instances[b:]

			trainDataSet.instances  = train
			testDataSet.instances	= test
	
			return trainDataSet, testDataSet

	def copy(self):
		dataSet = DataSet()
		dataSet.name 	  = self.name
		dataSet.headers   = self.headers
		dataSet.instances = self.instances
		dataSet.summary   = self.summary
		return dataSet
	
	def update(self):
		headerIndex = 0
		for header in self.headers:
			header.count 	= {}
			header.n 	= 0
			header.mode 	= ""
			header.most	= 0.0
			header.hi	= 0.0
			header.low	= 0.0
			header.mu	= 0.0
			header.m2	= 0.0
			header.sd	= 0.0
			instanceIndex = 0
			for instance in self.instances:
				header.n = len(self.instances)
				header.id = headerIndex
				instance.features[headerIndex].id = headerIndex
				if header.klass == True:
					self.klassLoc = headerIndex
				if header.numeric == True:
					instance.features[headerIndex].numeric = True
				if instance.features[headerIndex].numeric == True:
					if instance.features[headerIndex].value in header.count:
						header.count[instance.features[headerIndex].value] += 1
					else:
						header.count[instance.features[headerIndex].value] = 1
					header.mode = header.maxValueKey(header.count)[0]
					header.most = header.maxValueKey(header.count)[1]
					if instance.features[headerIndex].value.find('?') == -1:
						val = instance.features[headerIndex].value
					else:
						val = 0 #so a ? doesnt break everything
						header.n -= 1 #to account for no value
					if header.n == 0:
						header.n = 0.000000000001
						#print "..."
					header.m2 += float(val)
					header.mu = header.m2 / header.n 
					header.sd = math.sqrt((1.0/header.n)*(header.m2))
				if instance.features[headerIndex].numeric == False:
					if instance.features[headerIndex].value in header.count:
						header.count[instance.features[headerIndex].value] += 1
					else:
						header.count[instance.features[headerIndex].value] = 1
					header.mode = header.maxValueKey(header.count)[0]
					header.most = header.maxValueKey(header.count)[1]
				instanceIndex += 1
			headerIndex += 1
		
					
class Header:
	def __init__(self):
		self.id          = 0
		self.name	 = ""
		self.n		 = 0
		self.count	 = {}
		self.mode	 = ""
		self.most	 = ""
		self.hi		 = 0.0
		self.low	 = 0.0
		self.mu		 = 0.0
		self.m2		 = 0.0
		self.sd		 = 0.0
		self.flagged	 = False
		self.numeric	 = False
		self.klass	 = False
		self.max	 = False
		self.min	 = False
		self.frequencies = {}
	def maxValueKey(self, dictionary):
	#Returns the most common key [0] and the most common keys value [1]
	     	value	= list(dictionary.values())
	     	key	= list(dictionary.keys())
	     	return key[value.index(max(value))], dictionary[key[value.index(max(value))]]

class Instance:
	def __init__(self):
		self.id 	= 0
		self.features 	= []
		self.classVal	= None
				
class Feature:
	def __init__(self):
		self.id         = 0
		self.name 	= ''
		self.value 	= ''
		self.numeric	= False

			
		
