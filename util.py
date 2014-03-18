import os
import csv
import string
import math
import re
import collections
from structs import *

dataSetList = os.listdir('dataSets/') #List of accessible data-sets


def loadDataSet(dataSetName, flag):
	#Flags = 'yes', 'no', 'all'
	dataSet 	= DataSet()
	dataSet.name 	= dataSetName
	with open ('dataSets/' + dataSetName, 'rb') as csvfile:
		data = csv.reader(csvfile, delimiter = ',')
		start = 0
		for row in data:
			if row[0].find('##') != -1:
				break
			else: 
				header = Header()
				#print row
				row = "".join(row)
				#print row
				#row = row[:row.find('#')].strip()
				#print row
				header.name = row.strip()
				#print header.name
				if header.name.find('?') != -1:
					header.flagged = True
				if header.name.find('=') != -1:
					header.klass 	= True
					#print "found klass"
				if header.name.find('+') != -1:
					header.max	= True
				if header.name.find('-') != -1:
					header.min	= True
				if header.name.find('$') != -1:
					header.numeric	= True
				dataSet.headers.append(header)
				start += 1
		instID = 0
		for row in data:
			instance = Instance()
			instance.id = instID
			column 	= 0
			end 	= len(row) - 1
			rows 	= []
			if flag == "all":
				rows += row
			if flag == "yes":
				if row[end] == "yes":
					rows += row
			if flag == "no":
				if row[end] == "no":
					rows += row
			for col in rows:
				feature = Feature()
				feature.name = dataSet.headers[column].name
				feature.value = col.strip()
				instance.features.append(feature)
				column += 1
			instance.classVal = instance.features[end].value
			dataSet.instances.append(instance)
			instID += 1
		dataSet.update()
	return dataSet

def loadDataSetByKey(dataSetName, key):
	#Flags = 'yes', 'no', 'all'
	dataSet 	= DataSet()
	dataSet.name 	= dataSetName
	with open ('dataSets/' + dataSetName, 'rb') as csvfile:
		data = csv.reader(csvfile, delimiter = ',')
		start = 0
		for row in data:
			if row[0].find('##') != -1:
				break
			else: 
				header = Header()
				row = "".join(row)
				row = row[:row.find('#')].strip()
				header.name = row
				if header.name.find('?') != -1:
					header.flagged = True
				if header.name.find('=') != -1:
					header.klass 	= True
					header.klassLoc = start
				if header.name.find('+') != -1:
					header.max	= True
				if header.name.find('-') != -1:
					header.min	= True
				if header.name.find('$') != -1:
					header.numeric	= True
				dataSet.headers.append(header)
				start += 1
		instID = 0
		for row in data:
			instance = Instance()
			instance.id = instID
			column 	= 0
			end 	= len(row) - 1
			rows 	= []
			if key == "all":
				rows += row
			if row[end] == key:
				rows += row
			if len(rows) >= 1:
				for col in rows:
					feature = Feature()
					feature.name = dataSet.headers[column].name
					feature.value = col.strip()
					instance.features.append(feature)
					column += 1
				instance.classVal = instance.features[end].value
				dataSet.instances.append(instance)
				instID += 1
	return dataSet

def reloadDataSetByKey(dataSetObject):
	sets = []
	klassLoc = len(dataSetObject.instances[0].features) -1
	for key in dataSetObject.headers[klassLoc].count:
		ds = loadDataSetByKey(dataSetObject.name, key)
		ds.update()
		sets.append(ds)
	return sets

#Functions Relating to Modifying DataSet Objects

def createTrainTest(dataSetObject, folds, repeats):
	#Creates random training/test dataSets
	trainDataSets = []
	testDataSets = []
	if folds or repeats == 0:
		folds, repeats = 1, 1
	for _ in range(folds*repeats):
		sets = dataSetObject.split(folds)
		tempTrain = sets[0]
		tempTest = sets[1]
		trainDataSets.append(tempTrain)
		testDataSets.append(tempTest)
	return trainDataSets, testDataSets
		

#Functions Relating to Calculating or Finding Values

def maxValueKey(dictionary):
	#Returns the most common key [0] and the most common keys value [1]
     	value	= list(dictionary.values())
     	key	= list(dictionary.keys())
     	return key[value.index(max(value))], dictionary[key[value.index(max(value))]]

#Printing Functions
				
def printFullTable(dataSetObject):
	dataSetObject.update()
	headers = ""
	expected = ""
	certainty = ""
	for header in dataSetObject.headers:
		if header.numeric == True and header.flagged == False:
			headers += header.name.ljust(20)
			expected += str(header.mu).ljust(20)
			certainty += str(header.sd).ljust(20)
		elif header.numeric == False and header.flagged == False:
			headers += header.name.ljust(20)
			expected += str(header.mode).ljust(20)
			certainty += str((float(header.most)/header.n)).ljust(20)
	print headers
	print expected
	print certainty
	for instance in dataSetObject.instances:
		instances = ""
		index = 0
		for feature in instance.features:
			if dataSetObject.headers[index].flagged == False:
				instances += str(feature.value).ljust(20)
			index += 1
		if instances != '':
			print instances

#Decision Tree Support functions		
def unique(lst):
	#Removes redundant values in a list
    
	lst = lst[:]
	unique_lst = []

	#Cycle through the list and add each value to the unique list only once.
	for item in lst:
        	if unique_lst.count(item) <= 0:
            		unique_lst.append(item)
            
   	#Return the list with all redundant values removed.
 
	return unique_lst

def getValues(data, attr):
	#Creates a list of values in the chosen attribute for each record in data,
	#and removes redundant values 
  
	data = data[:]
	return unique([record[attr] for record in data])	

def getData(ds, attributes):
	#Takes a dataSetObject and a list of attributes (header names) and returns a dictionary object with all the data
	ds = ds.copy()
	# Parse all of the individual data records from the given file
	data = []
	for instance in ds.instances:
		data.append(dict(zip(attributes, [feat.value.strip() for feat in instance.features])))
	return data		

def getExamples(data, attr, value):
	#Returns a list of values where data has attr
	data = data[:]
	lst = []
    
    	if not data:
        	return lst
   	else:
        	record = data.pop()
        if record[attr] == value:
		lst.append(record)
		lst.extend(getExamples(data, attr, value))
		return lst
        else:
		lst.extend(getExamples(data, attr, value))
		return lst

def getAttributes(ds):
	#Returns a list of attributes (header names)
	#Create a list of all the lines in the training file
	ds = ds.copy()
	attributes = [header.name for header in ds.headers]
	for name in attributes:
		if name.find("?") != -1:
			attributes.remove(name)
	#print attributes
	return attributes

def nextBestAttr(data, attributes, target, fitness):
   	#Returns attribute with best infogain
	data = data[:]
	best = 0.0
	battr = None

	for attr in attributes:
		gain = fitness(data, attr, target)
		if (gain >= best and attr != target):
		    best = gain
		    battr = attr
                
   	return battr

def most(lst):
	#returns most frequent item
	lst = lst[:]
	highest = 0
	most = None
	for val in unique(lst):
        	if lst.count(val) > highest:
			most = val
			highest = lst.count(val)     
    	return most

def printDT(tree, strn):
    #Prints a Decison Tree recursively
	if type(tree) == dict and type(tree) != str:
		print "%s%s" % (strn, tree.keys()[0])
		for item in tree.values()[0].keys():
		    print "%s\t%s" % (strn, item)
		    printDT(tree.values()[0][item], strn + "\t")
	else:
       	 	print "%s\t->\t%s" % (strn, tree)

#Decison Tree Fitness Function and misc
def entropy(data, target):
	#Calculates the entropy of the given data set for the target attribute.

	valFreq = {}
	ent = 0.0

    	#Calculate the frequency of each of the values in the target attr
    	for record in data:
		if (valFreq.has_key(record[target])):
           		valFreq[record[target]] += 1.0
        	else:
            		valFreq[record[target]] = 1.0

    #Calculate the entropy of the data for the target attribute
	for freq in valFreq.values():
        	ent += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
	return ent
    
def infogain(data, attr, target):
	#Calculates the information gain (reduction in entropy) that would
	#result by splitting the data on the chosen attribute (attr).
  
	val_freq = {}
	subset_entropy = 0.0

	# Calculate the frequency of each of the values in the target attribute
	for record in data:
		if (val_freq.has_key(record[attr])):
            		val_freq[record[attr]] += 1.0
		else:
           		 val_freq[record[attr]] = 1.0

	# Calculate the sum of the entropy for each subset of records weighted
	# by their probability of occuring in the training set.
	for val in val_freq.keys():
		val_prob = val_freq[val] / sum(val_freq.values())
		data_subset = [record for record in data if record[attr] == val]
		subset_entropy += val_prob * entropy(data_subset, target)

	#Subtract the entropy of the chosen attribute from the entropy of the
	#whole data set with respect to the target attribute (and return it)
	return (entropy(data, target) - subset_entropy)

#OTHER MISC
def is_empty(struct):
    if struct:
        return False
    else:
        return True
			
def runTests():
	print "Running Tests..."
	test = loadDataSet(dataSetList[1], "all")
	#printFullTable(test)
	sets = reloadDataSetByKey(test)
	#printFullTable(sets[0])
	#printFullTable(sets[1])
	#printFullTable(sets[2])
	#test2 = createTrainTest(test, 2, 2)
	#test3 = test2[0][0]
	#test3.update()
	#printFullTable(test3)
	#printNoTable(test)
	print "Finished running tests..."

#runTests()
