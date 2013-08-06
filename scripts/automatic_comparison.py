import sys
import difflib
import collections
import re
import math
import os
import numpy
import array
# import Pycluster
import shutil
import re
from sklearn.cluster import AffinityPropagation
from random import randint

#Run a straight up diff between the two text files, very slow
def stringDiffComparison(fname1, fname2):
	with open(fname1, "r") as fh1:
		with open(fname2, "r") as fh2:
			differ = difflib.Differ()
			return len(list(differ.compare(fh1.read(), fh2.read())))

#Compare the differences in how many times a word appears in each file
def bagWordComparison(fname1, fname2):
	with open(fname1, "r") as fh1:
		with open(fname2, "r") as fh2:
			texts = [fh1.read(), fh2.read()]
			bagsofwords = [collections.Counter(re.findall(r'\w+', txt)) for txt in texts]
			score = 0
			for word in bagsofwords[0]:
				score  = score + math.fabs(bagsofwords[0][word] - bagsofwords[1][word])
			for word in bagsofwords[1]:
				if bagsofwords[0][word] == 0:
					score = score + bagsofwords[1][word]
	return score
	
#Check for the Alice API calls move, turn and roll and do a sring DNA comparison between them
def apiCallComparison(fname1, fname2):
	with open(fname1, "r") as fh1:
		with open(fname2, "r") as fh2:
			words1 = fh1.read().split()
			words2 = fh2.read().split()
			apiwords1 = []
			apiwords2 = []
			d = 1
			for word in words1:
				if word == "MoveAnimation:" or word == "TurnAnimation:" or word == "RollAnimation:":
					apiwords1.append(word)
			for word in words2:
				if word == "MoveAnimation:" or word == "TurnAnimation:" or word == "RollAnimation:":
					apiwords2.append(word)
			F = [[0 for i in range(len(apiwords2))] for j in range(len(apiwords1))]
			l1 = len(apiwords1)
			l2 = len(apiwords2)
			if l1 > 0 and l2 > 0:
				for i in range(l2):
					F[0][i] = d*i
				for j in range(l1):
					F[j][0] = d*j
				for i in range(1, l1):
					for j in range(1, l2):
						if apiwords1[i] == apiwords2[j]:
							F[i][j] = min(F[i-1][j-1], F[i-1][j] + 1, F[i][j-1] + 1)
						else:
							F[i][j] = min(F[i-1][j-1] + 1, F[i-1][j] + 1, F[i][j-1] + 1)
				return F[l1-1][l2-1]	
			else:
				return max(l1, l2)
			

	
def astSimilarityComparison(fname1, fname2):
	return 0
	
#Specific comparison done for the dancing bunny comparison	
def dancingBunnyComparison(fname1, fname2):
	with open(fname1, "r") as fh1:
		with open(fname2, "r") as fh2:
			#Divide the text into lines
			lines1 = fh1.read().split('\n')
			lines2 = fh2.read().split('\n')
			whileCount1 = 0
			whileCount2 = 0
			paramColl1 = []
			paramColl2 = []
			methodNames1 = []
			methodNames2 = []
			for line in lines1:
				#Count the nr of loops
				if "Loop" in line:
					whileCount1 += 1
				#Count the nr of parameters for each method
				if "MethodCall" in line:
					params = []
					nextName = False
					for word in line.split():
						if nextName:
							methodNames1.append(word)
						if word == "MethodCall:":
							nextName = True
						else:
							nextName = False
						if "param" in word:
							params.append(word)
					paramColl1.append(params)
			for line in lines2:
				if "Loop" in line:
					whileCount2 += 1
				if "MethodCall" in line:
					params = []
					nextName = False
					for word in line.split():
						if nextName:
							methodNames2.append(word)
						if word == "MethodCall:":
							nextName = True
						else:
							nextName = False
						if "param" in word:
							params.append(word)
					paramColl2.append(params)
	#Compare the nr of while loops
	whileScore = math.fabs(whileCount1 - whileCount2)
	paramScore = 0
	#Compare nr of parameters for each method
	for i in range(len(methodNames1)):
		try:
			index = methodNames2.index(methodNames1[i])
			paramScore += math.fabs(len(paramColl1[i]) - len(paramColl2[index]))
			paramColl2.pop(index)
			methodNames2.pop(index)
		except ValueError:
			paramScore += len(paramColl1)
		
	for i in range(len(methodNames2)):
		try:
			index = methodNames1.index(methodNames2[i])
		except ValueError:
			paramScore += len(paramColl2[i])
	
	lengthScore = math.fabs(len(lines1) - len(lines2))
	# print "While: " + str(whileScore)
	# print "Param: " + str(paramScore)
	# print "Length: " + str(lengthScore)
	return 10 * whileScore + paramScore + lengthScore/5.0

#Sum all of the comparisons 
def automaticComparison(fname1, fname2):
	stringDiffScore = 0
	bagWordScore = 0
	apiCallScore = 0
	astSimilarityScore = 0
	dancingBunnyScore = 0
	# stringDiffScore = stringDiffComparison(fname1, fname2)	
	# bagWordScore = bagWordComparison(fname1, fname2)
	# apiCallScore = apiCallComparison(fname1, fname2)
	# astSimilarityScore = astSimilarityComparison(fname1, fname2)
	dancingBunnyScore = dancingBunnyComparison(fname1, fname2)
	totalScore = stringDiffScore + 18 * bagWordScore + 270 * apiCallScore + astSimilarityScore + dancingBunnyScore
	# totalScore = totalScore / 4000
	return totalScore
	
def kmeans(folder):
	if folder[-1] != '/':
		folder = folder + '/'
	files = []
	for assignment in os.listdir (folder):
		notUsed, fileExtension = os.path.splitext(assignment)
		if fileExtension == ".txt":
			files.append(assignment)
	
	files.sort(key=lambda x: [int(x.split('.')[i]) for i in range(len(x.split('.'))-1)])
	
	randFiles = files[:1000]
		
		
	print "List constructed"
		
	l = len(randFiles)
	distances = []
	print "Random list constructed"
	
	# Used for Affinity propagation
	m = [[1 for i in range(l)] for j in range(l)]
	
	for i in range(l):
		for j in range(i+1, l):
			# sim = math.exp(-automaticComparison(folder + randFiles[i], folder + randFiles[j])/100.0)
			sim = -automaticComparison(folder + randFiles[i], folder + randFiles[j])
			# if sim > 0.05:
				# m[i][j] = sim
				# m[j][i] = sim
			# else:
				# m[i][j] = 0
				# m[j][i] = 0
			m[i][j] = sim
			m[j][i] = sim

# Used for kmedoids
#	for i in range(l):
#		for j in range(i+1, l):
#			distances.append(automaticComparison(folder + randFiles[i], folder + randFiles[j]))
#
	print "Distances calculated"
	print "Max distance: " + str(max(max(m)))
	print "Avarage distance: " + str(numpy.mean(m))

#
#	a = numpy.array(distances, float)
	a = numpy.array(m, float)
	print "Array constructed"
#	labels, error, nfound = Pycluster.kmedoids(distances, 8, 5)
#	print "K-medoids run"
	# p = [[-.5 for i in range(l)] for j in range(l)]
	af = AffinityPropagation(preference = -float(205000), damping = .9).fit(a)
	print "Affinity propagation run"
	clusters = af.cluster_centers_indices_
	print "Number of clusters: " + str(len(clusters))
	print clusters
	labels = af.labels_
	
	
	#Moves the files based on which cluster they ended up in
	if PC:
		resultPath = "C:/cygwin/home/Johan/AliceDataCompared/"
	else:
		resultPath = "/Users/Johan/Documents/AliceResults/"
	
	if os.path.exists(resultPath):
		shutil.rmtree(resultPath)
	os.makedirs(resultPath)
	os.makedirs(resultPath + "labels/")
	os.makedirs(resultPath + "transitions/")
	for i in range(len(clusters)):
		os.makedirs(resultPath + str(i))
	
	for cluster in clusters:
		shutil.copyfile(folder + randFiles[cluster], resultPath + "labels/" + randFiles[cluster])

	#Print the order of states a user will go through
	prev = None
	labelChain = ["State transitions for each user:"]
	labelChains = []
	transitionProb = [[0 for j in range(len(clusters))] for i in range(len(clusters)+1)]
	for i in range(len(randFiles)):
		curr = re.split('\.', randFiles[i])[0]
		if curr == prev:
			if labels[i] != labelChain[-1]:
				if len(labelChain) > 1:
					transitionProb[labelChain[-1]][labels[i]] += 1
				else:
					transitionProb[-1][labels[i]] += 1
				labelChain.append(labels[i])
		else:
			labelChains.append(labelChain)
			labelChain = ["State transitions for " + curr + ": "]			
			
		prev = curr
		shutil.copyfile(folder + randFiles[i], resultPath + str(labels[i]) + '/' + randFiles[i])
	labelChains.append(labelChain)
	print labelChains
	
	labelFile = open(resultPath + "transitions/labelChains.txt", "wb")
	print transitionProb
	for j in range(len(clusters)):
		sum = float(numpy.sum([row[j] for row in transitionProb]))
		print "Sum is: " + str(sum)
		for i in range(len(clusters)):
			if sum > 0:
				transitionProb[i][j] /= sum
			else:
				transitionProb[i][j] = float('nan')
				
	for j in range(len(clusters)):
		print [row[j] for row in transitionProb]
		
	for lc in labelChains:
		for l in lc:
			labelFile.write(str(l) + " ")
		labelFile.write('\n')
		
	
	labelFile.close()
	
	# checkDistances(resultPath)
	
	
def checkDistances(path):
	for folder in os.listdir(path):
		print "Folder name: " + folder
		print "Scores:"
		for file1 in os.listdir(path + folder):
			for file2 in os.listdir(path + folder):
				print(automaticComparison(path + folder + '/' + file1, path + folder + '/' + file2))
	
	
if len(sys.argv) > 0:
    # kmeans(sys.argv[1])
	PC = True
	if PC:
		kmeans("C:/cygwin/home/Johan/AliceDataFlattened/9/")
	else:
		kmeans("/Users/Johan/Documents/AliceData/2_4/")
	# print automaticComparison("C:/cygwin/home/johan/AliceDataFlattened/9/6.225.txt", "C:/cygwin/home/johan/AliceDataFlattened/9/3.71.txt")
else:
    print "Gimme more arguments"