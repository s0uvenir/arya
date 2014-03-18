from structs import *
from util import *
from learners import *



def runLearner(dataSetObject, learners, folds, repeats):
	sets = createTrainTest(dataSetObject, folds, repeats)
	trainResultsPred = []
	trainResultsAcc  = []
	testResultsPred  = []
	testResultsAcc 	 = []
	results = ""
	
	for learner in learners:
		if folds or repeats == 0:
			folds = 1
			repeats = 1
		for i in range(folds*repeats):
			if learner == "zeroR":
				if i == 0:
					results += "\nzeroR: "+ dataSetObject.name + "\n"
				run = zeroR(dataSetObject) #Run Learner on Full Set
				fullPred  = run[0]
				fullAcc   = run[1]
			
				selected = sets[0][i]
				selected.update() #Force Header update just in case (can remove once verified)
				run = zeroR(selected) #Run Learner on Training Set
				trainPred = run[0]
				trainAcc  = run[1]
				trainResultsPred.append(trainPred)
				trainResultsAcc.append(trainAcc)
			
				selected = sets[1][i]
				selected.update() #Force Header update just in case (can remove once verified)
				run = zeroR(selected) #Run Learner on Test Set
				testPred = run[0]
				testAcc  = run[1]
				testResultsPred.append(testPred)
				testResultsAcc.append(testAcc)
				results += ' %.3f' % testAcc

			if learner == "NB":
				if i == 0:
					results += "\nNB: " + dataSetObject.name + "\n"
				train = sets[0][i]
				test = sets[1][i]
				run = NB(train,test) #Run Learner on Full Set
				testResultsAcc.append(run)
				results += ' %.3f' % run

			if learner == "DT":
				if i == 0:
					results += "\nDT: " + dataSetObject.name + "\n"
				
				
				train = sets[0][0]
				test  = sets[1][0]
				attributes = getAttributes(dataSetObject)
				target = attributes[:-1]
				#data = getData(dataSetObject, attributes)
				#run = DT(train, test)
				print attributes
				dt = createDT(dataSetObject, attributes, target, gain)
				printDT(dt, "")
				
	avg = 0
	sum = 0
	for result in testResultsAcc:
		sum += result
		avg = sum/len(testResultsAcc)
	print results
	print "Median ACC = " + str(avg) + "\n"

			
		

def generateReports(dataSetObject, folds, repeats):
	sets = createTrainTest(dataSetObject, folds, repeats)
	for i in range(folds*repeats):
		print "\n**** Training Set %s ****" % i
		selected = sets[0][i]
		selected.update()
		printFullTable(selected)
		print "\n**** Test Set %s ****" % i
		selected = sets[1][i]
		selected.update()
		printFullTable(selected)
 

ds = loadDataSet(dataSetList[3], "all")
#print type(ds)
attributes = getAttributes(ds)
data = getData(ds, attributes)
target = attributes[-1]
tree = createDT(data, attributes, target, infogain)
printDT(tree, "")
#runLearner(ds, ["DT"], 0,0)
#runLearner(ds, ["zeroR"], 5,5)
#ds = loadDataSet(dataSetList[2], "all")
#runLearner(ds, ["NB"], 5,5)
#runLearner(ds, ["zeroR"], 5,5)
#ds = loadDataSet(dataSetList[3], "all")
#runLearner(ds, ["NB"], 5,5)
#runLearner(ds, ["zeroR"], 5,5)
#printFullTable(ds)
#print "\n"
#ds = reloadDataSetByKey(ds, 'yes')
#printFullTable(ds)
#print "\n"
#ds = loadDataSet(dataSetList[3], "all")
#ds = reloadDataSetByKey(ds, 'no')
#printFullTable(ds)
#generateReports(ds, 2, 2)
#runLearner(ds, ["zeroR"], 2,2)
#ds = loadDataSet(dataSetList[0], "all")
#runLearner(ds, ["zeroR"], 2,2,ds,ds)

