import sys
import os
from filecomparison import fileComparison
#APICall = 16000
#BoW = 60000
#Specialized = 2400000
#Balanced = 24000000
#Belanced coeff = BOW: 1, API: 0.5, SPEC: 6 

basePath = "C:/cygwin/home/Johan/AliceDataClusters/"
refPath = "C:/cygwin/home/Johan/AliceReferences/"
stuckPath = refPath + "stuck/"
notStuckPath = refPath + "notStuck/"
afPath = basePath + "AffinityPropagation/"
kmPath = basePath + "KMedoids/"

def functionComparison(function, stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam):
	pairComparison(afPath + function + '/labels/', stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam)
	# pairComparison(kmPath + function + '/labels/', stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam)
	
def pairComparison(folder2, stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam):
	stuckClust = subComparison(stuckPath, folder2, stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam)
	notStuckClust = subComparison(notStuckPath, folder2, stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam)
	
	common = 0
	unique1 = 0
	unique2 = 0
	for clust in stuckClust:
		if clust in notStuckClust:
			common += 1
		else:
			unique1 +=1
				
	for clust in notStuckClust:
		if clust not in stuckClust:
			unique2 += 1
	print "Common: " + str(common)
	print "Unique in stuck: " + str(unique1)
	print "Unique in not stuck: " + str(unique2)
	
def subComparison(folder1, folder2, stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam):		
	min = float('inf')
	clust = -1
	foundClust = []
	for file1 in os.listdir(folder1):
		currClust = 0	
		for file2 in os.listdir(folder2):
			dist = fileComparison(folder1 + file1, folder2 + file2, 
				stringDiffParam, bagWordParam, apiCallParam, dancingBunnyParam)
			if dist < min:
				min = dist
				clust = currClust
			currClust += 1
		if clust not in foundClust:
			foundClust.append(clust)
	print "Number of clusters: " + str(len(foundClust))
	return foundClust
		
		
functionComparison("BoW", 0, 1, 0, 0)
functionComparison("APICall", 0, 0, 1, 0)
functionComparison("Specialized", 0, 0, 0, 1)
functionComparison("Balanced", 0, 1, 0.5, 6)