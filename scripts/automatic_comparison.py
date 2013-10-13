import sys
import difflib
import collections
import re
import math
import os
import numpy
import array
import xlwt
import Pycluster
import shutil
import re
from sklearn.cluster import AffinityPropagation
from random import randint
from scipy.sparse import bsr_matrix

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
	bagWordScore = bagWordComparison(fname1, fname2)
	apiCallScore = apiCallComparison(fname1, fname2)
	# astSimilarityScore = astSimilarityComparison(fname1, fname2)
	dancingBunnyScore = dancingBunnyComparison(fname1, fname2)
	totalScore = stringDiffScore + 18 * bagWordScore + 270 * apiCallScore + astSimilarityScore + dancingBunnyScore
	# totalScore = dancingBunnyScore
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
	
	randFiles = files[:4025]
		
		
	
		
	l = len(randFiles)
	print "List constructed, length: " + str(l)
	print "Original length: " + str(len(files))
	
	# Used for Affinity propagation
	# m = [[1 for i in range(l)] for j in range(l)]
	#m = bsr_matrix((l,l), dtype=int);
	m = numpy.array([[0 for i in range(l)] for j in range(l)])
	
	for i in range(l):
		for j in range(i+1, l):
			# sim = -math.exp(automaticComparison(folder + randFiles[i], folder + randFiles[j])/100.0)
			sim = -(automaticComparison(folder + randFiles[i], folder + randFiles[j]))
			# if sim > 0.05:
				# m[i][j] = sim
				# m[j][i] = sim
			# else:
				# m[i][j] = 0
				# m[j][i] = 0
			m[i][j] = sim
			m[j][i] = sim

	print "Distances calculated"

	print "Array constructed"
	print "Mean: " + str(numpy.mean(m))
	
	
	
	# labels, error, nfound = Pycluster.kmedoids(m, 16, 5)
	# print "K-medoids run, labels: "
	# print labels
	# clusters = []
	# for l in labels:
		# if l not in clusters:
			# clusters.append(l)
	# print "Number of clusters: " + str(len(clusters))
	
	# i = 0
	# for c in clusters:
		# j = 0
		# for l in labels:
			# if l == c:
				# labels[j] = i
			# j += 1
		# clusters[i] = i
		# i += 1
		
	
	p = [[-.5 for i in range(l)] for j in range(l)]
	# Spec: 205000
	# Api: 200000
	af = AffinityPropagation(preference = float(1000000 * numpy.mean(m)), damping = .9).fit(m)
	labels = af.labels_
	print "Affinity propagation run, labels: "
	print labels
	clusters = af.cluster_centers_indices_
	print "Number of clusters: " + str(len(clusters))
	print clusters
	
	
	#Moves the files based on which cluster they ended up in
	if PC:
		resultPath = "C:/cygwin/home/Johan/AliceDataCompared/"
	else:
		resultPath = "/Users/Johan/Documents/AliceResults/"
	
	xlsfolder = "C:/cygwin/home/Johan/AliceDataXLS/"
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
	for j in range(len(clusters)):
		sum = float(numpy.sum([row[j] for row in transitionProb]))
		for i in range(len(clusters)):
			if sum > 0:
				transitionProb[i][j] /= sum
			else:
				transitionProb[i][j] = float('nan')
				
		
	
	
	book = xlwt.Workbook()
	sh1 = book.add_sheet("State transitions")
	sh2 = None
	sh3 = None
	sh = sh1
	font = xlwt.Font()
	style = xlwt.XFStyle()
	font.bold = True
	style.font = font
	sh.write(0, 0, "In/Out", style)
	for i in range(len(transitionProb)-1):
		sh.write(i+1, 0, str(i+1), style)
	sh.write(len(transitionProb), 0, "Start", style)
	k = 0
	for j in range(len(transitionProb[0])):
		if k >= 511:
			if not sh3:
					sh3 = book.add_sheet("State transitions - cont 2")
			sh3.write(0, k-511, str(k+1), style)
		elif k >= 255:
			if not sh2:
					sh2 = book.add_sheet("State transitions - cont")
			sh2.write(0, k-255, str(k+1), style)
		else:
			sh1.write(0, k+1, str(k+1), style)
		k += 1
	i = 1
	sh = sh1
	for lc in transitionProb:
		j = 1
		for l in lc:
			if j >= 512:
				if not sh3:
					sh3 = book.add_sheet("State transitions - cont 2")		
				sh3.write(i, j-512, str(l))
			elif j >= 256:				
				if not sh2:
					sh2 = book.add_sheet("State transitions - cont")		
				sh2.write(i, j-256, str(l))
			else:
				sh1.write(i, j, str(l))
			#print "About to write, i = " + str(i) + ", j = " + str(j)
			j += 1
		i += 1
	
	sh1 = book.add_sheet("Transition chains")
	sh2 = None
	sh3 = None
	i = 0
	j = 0
	
	
	stats = [len(lc) for lc in labelChains]
	for lc in labelChains:
		for l in lc:
			if j >= 512:
				if not sh3:
					sh3 = book.add_sheet("Transition chains - cont")
				sh3.write(i, j-512, l)
			elif j >= 256:
				if not sh2:
					sh2 = book.add_sheet("Transition chains - cont")
				sh2.write(i, j-256, l)
			else:
				sh1.write(i, j, l)
			j += 1
		i += 1
		j = 0
	
	sh = book.add_sheet("Metadata")
	
	noCluster = len(transitionProb) - 1
	meanNos = numpy.mean(stats)
	medianNos = numpy.median(stats)
	maxNos = numpy.max(stats)
	minNos = numpy.min(stats)
	
	numLinkedStates = 0
	numSimilarStates = 0
	numTransitions = 0
	numLiveTransitions = 0
	numDeadTransitions = 0
	for cl in transitionProb:
		for c in cl:
			if c == 1:
				numLinkedStates += 1
			elif c > 0.85:
				numSimilarStates += 1
			numTransitions += 1
			if c == 0:
				numDeadTransitions += 1
			else:
				numLiveTransitions += 1
	
	print noCluster
	print meanNos
	print medianNos
	print maxNos
	print minNos
	print numLinkedStates
	print numSimilarStates
	print numDeadTransitions
	sh.write(0, 0, "Number of clusters")
	sh.write(0, 1, str(noCluster))
	sh.write(1, 0, "Mean number of states")
	sh.write(1, 1, str(meanNos))
	sh.write(2, 0, "Median number of states")
	sh.write(2, 1, str(medianNos))
	sh.write(3, 0, "Max number of states")
	sh.write(3, 1, str(maxNos))
	sh.write(4, 0, "Min number of states")
	sh.write(4, 1, str(minNos))
	sh.write(5, 0, "Number of joined states")
	sh.write(5, 1, str(numLinkedStates))
	sh.write(6, 0, "Number of similar states")
	sh.write(6, 1, str(numSimilarStates))
	sh.write(7, 0, "Number of transitions")
	sh.write(7, 1, str(numTransitions))
	sh.write(8, 0, "Number of taken transitions")
	sh.write(8, 1, str(numLiveTransitions))
	sh.write(9, 0, "Number of untaken transitions")
	sh.write(9, 1, str(numDeadTransitions))

	
	
	labelFile.write("\\begin{table}\n")	
	labelFile.write("\\centering\n")
	labelFile.write("\\begin{tabular}{|l|l|}\n\\hline\n")
	labelFile.write("\\textbf{" + name + "} & \\textbf{Result}\\\\\n\\hline\n")
	
	labelFile.write("Number of clusters & " + str(noCluster) + '\\\\\n')
	labelFile.write("Mean number of states & " + str(medianNos) + '\\\\\n')
	labelFile.write("Median number of states & " + str(noCluster) + '\\\\\n')
	labelFile.write("Max number of states & " + str(maxNos) + '\\\\\n')
	labelFile.write("Min number of states & " + str(minNos) + '\\\\\n')
	labelFile.write("Number of joined states & " + str(numLinkedStates) + '\\\\\n')
	labelFile.write("Number of similar states & " + str(numSimilarStates) + '\\\\\n')
	labelFile.write("Number of transitions & " + str(numTransitions) + '\\\\\n')
	labelFile.write("Number of taken transitions & " + str(numLiveTransitions) + '\\\\\n')
	labelFile.write("Number of untaken transitions & " + str(numDeadTransitions) + '\\\\\n')
	
	labelFile.write("\\hline\n")
	labelFile.write("\\end{tabular}\n")
	labelFile.write("\\label{TODO}\n")
	labelFile.write("\\caption{TODO}\n")
	labelFile.write("\\end{table}\n")
	labelFile.write("\n\n\n")
	
	
	book.save(xlsfolder + name + ".xls")
	labelFile.close()
	# checkDistances(resultPath)
	
	
def checkDistances(path):
	for folder in os.listdir(path):
		print "Folder name: " + folder
		print "Scores:"
		for file1 in os.listdir(path + folder):
			for file2 in os.listdir(path + folder):
				print(automaticComparison(path + folder + '/' + file1, path + folder + '/' + file2))
	
	s
if len(sys.argv) > 0:
    # kmeans(sys.argv[1])
	PC = True
	name = "AffinityBalanced" 
	if PC:
		kmeans("C:/cygwin/home/Johan/AliceDataFlattened/9/")
	else:
		kmeans("/Users/Johan/Documents/AliceData/2_4/")
	# print automaticComparison("C:/cygwin/home/johan/AliceDataFlattened/9/6.225.txt", "C:/cygwin/home/johan/AliceDataFlattened/9/3.71.txt")
else:
    print "Gimme more arguments"