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
import gc
from sklearn.cluster import AffinityPropagation
from random import randint
from scipy.sparse import bsr_matrix
from filecomparison import fileComparison


name = "dummy"
numFilesToCluster = 100
affinityPreference = 16000
folder = "C:/cygwin/home/Johan/AliceDataFlattened/9/"
resultPathBase = "C:/cygwin/home/Johan/AliceDataClusters/"
xlsPathBase = "C:/cygwin/home/Johan/AliceDataXLS/"

files = []
for assignment in os.listdir (folder):
	notUsed, fileExtension = os.path.splitext(assignment)
	if fileExtension == ".txt":
		files.append(assignment)

files.sort(key=lambda x: [int(x.split('.')[i]) for i in range(len(x.split('.'))-1)])

#Number of files we want to compare
filesToCluster = files[:numFilesToCluster]

numFiles = len(filesToCluster)
rangeFiles = range(numFiles)
print "Clustered file list constructed, length: " + str(numFiles)
print "Full length: " + str(len(files))

def cluster():
	m = numpy.array([[0 for i in rangeFiles] for j in rangeFiles])

	for i in rangeFiles:
		for j in range(i+1, numFiles):
			distance = float(fileComparison(folder + filesToCluster[i], folder + filesToCluster[j]))
			# Square to minimize quadratic error
			# distanceSquared = distance * distance
			m[i][j] = distance
			m[j][i] = distance

	print "Distances matrix calculated"
	print "Median of matrix: " + str(numpy.median(m))

	labels, clusters = kmedoids(m)
	print "Labels:"
	print labels
	print "Clusters:"
	print clusters
	print "K-medoids run, number of clusters: " + str(len(clusters))

	moveFiles(filesToCluster, labels, clusters, "KMedoids/")

	#Negate since affinity propagation works on negative distance values
	m = -m
	gc.collect()
	labels, clusters = affinityPropagation(m)
	print "Affinity propagation run, number of clusters: " + str(len(clusters))

	moveFiles(filesToCluster, labels, clusters, "AffinityPropagation/")

def kmedoids(m):
	labels, error, nfound = Pycluster.kmedoids(m, 16, 5)

	# Find the clusters and rename to have same naming convention as affinity propagation
	clusters = []
	for label in labels:
		if label not in clusters:
			clusters.append(label)

	currentCluster = 0
	for cluster in clusters:
		currentLabel = 0
		for label in labels:
			if label == cluster:
				labels[currentLabel] = currentCluster
			currentLabel += 1
		# clusters[currentCluster] = currentCluster
		currentCluster += 1
	return labels, clusters

def affinityPropagation(m):
	af = AffinityPropagation(preference = float(affinityPreference * numpy.median(m)), damping = .9).fit(m)
	labels = af.labels_
	clusters = af.cluster_centers_indices_
	return labels, clusters


def moveFiles(filesToCluster, labels, clusters, endOfFilePath):

	resultPath = resultPathBase + endOfFilePath + name + '/'
	xlsPath = xlsPathBase + endOfFilePath

	lenClusters = len(clusters)
	rangeClusters = range(lenClusters)

	# Moves the files based on which cluster they ended up in
	if os.path.exists(resultPath):
		shutil.rmtree(resultPath)
	os.makedirs(resultPath)
	os.makedirs(resultPath + "labels/")
	os.makedirs(resultPath + "transitions/")
	for i in rangeClusters:
		os.makedirs(resultPath + str(i))

	for cluster in clusters:
		shutil.copyfile(folder + filesToCluster[cluster], resultPath + "labels/" + filesToCluster[cluster])
	#Print the order of states a user will go through
	prev = None
	labelChain = ["State transitions for each user:"]
	labelChains = []
	clusterCount = [0 for i in rangeClusters]
	transitionProb = [[0 for j in rangeClusters] for i in range(lenClusters+1)]
	for i in rangeFiles:
		curr = re.split('\.', filesToCluster[i])[0]
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
		shutil.copyfile(folder + filesToCluster[i], resultPath + str(labels[i]) + '/' + filesToCluster[i])
		clusterCount[labels[i]] += 1

	print "Cluster count:"
	print clusterCount
	labelChains.append(labelChain)

	for j in rangeClusters:
		sum = float(numpy.sum([row[j] for row in transitionProb]))
		for i in rangeClusters:
			if sum > 0:
				transitionProb[i][j] /= sum
			else:
				transitionProb[i][j] = float('nan')

	book = xlwt.Workbook()
	sh1 = book.add_sheet("State transitions")

	font = xlwt.Font()
	style = xlwt.XFStyle()
	font.bold = True
	style.font = font

	sh1.write(0, 0, "In/Out", style)
	for i in range(len(transitionProb)-1):
		sh1.write(i+1, 0, str(i+1), style)
	sh1.write(len(transitionProb), 0, "Start", style)

	sh2 = None
	sh3 = None
	for j in range(len(transitionProb[0])):
		# Excel only supports 256 columns
		if j >= 511:
			if not sh3:
					sh3 = book.add_sheet("State transitions - cont 2")
			sh3.write(0, j-511, str(j+1), style)
		elif j >= 255:
			if not sh2:
					sh2 = book.add_sheet("State transitions - cont")
			sh2.write(0, j-255, str(j+1), style)
		else:
			sh1.write(0, j+1, str(j+1), style)


	i = 1
	for lc in transitionProb:
		j = 1
		for l in lc:
			# Excel only supports 256 columns
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
			j += 1
		i += 1


	sh1 = book.add_sheet("Transition chains")
	sh2 = None
	sh3 = None
	i = 0
	for lc in labelChains:
		j = 0
		for l in lc:
			# Excel only supports 256 columns
			if j >= 512:
				if not sh3:
					sh3 = book.add_sheet("Transition chains - cont 2")
				sh3.write(i, j-512, l)
			elif j >= 256:
				if not sh2:
					sh2 = book.add_sheet("Transition chains - cont")
				sh2.write(i, j-256, l)
			else:
				sh1.write(i, j, l)
			j += 1
		i += 1

	sh = book.add_sheet("Metadata")

	stats = [len(lc) for lc in labelChains]
	noCluster = len(transitionProb) - 1
	meanNol = numpy.mean(clusterCount)
	medianNol = numpy.median(clusterCount)
	maxNol = numpy.max(clusterCount)
	minNol = numpy.min(clusterCount)
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
			if c != 0:
				numLiveTransitions += 1
			else:
				numDeadTransitions += 1

	print "Number of clusters: " + str(noCluster)
	print "Mean number of labels: " + str(meanNol)
	print "Median number of labels: " + str(medianNol)
	print "Max number of labels: " + str(maxNol)
	print "Min number of labels: " + str(minNol)
	print "Mean number of states: " + str(meanNos)
	print "Median number of states: " + str(medianNos)
	print "Max number of states: " + str(maxNos)
	print "Min number of states: " + str(minNos)
	print "Number of joined states: " + str(numLinkedStates)
	print "Number of similar states: " + str(numSimilarStates)
	print "Number of transitions: " + str(numTransitions)
	print "Number of taken transitions: " + str(numLiveTransitions)
	print "Number of untaken transitions: " + str(numDeadTransitions)
	sh.write(0, 0, "Number of clusters")
	sh.write(0, 1, str(noCluster))
	sh.write(1, 0, "Mean number of labels")
	sh.write(1, 1, str(meanNol))
	sh.write(2, 0, "Median number of labels")
	sh.write(2, 1, str(medianNol))
	sh.write(3, 0, "Max number of labels")
	sh.write(3, 1, str(maxNol))
	sh.write(4, 0, "Min number of labels")
	sh.write(4, 1, str(minNol))
	sh.write(5, 0, "Mean number of labels")
	sh.write(5, 1, str(meanNos))
	sh.write(6, 0, "Median number of states")
	sh.write(6, 1, str(medianNos))
	sh.write(7, 0, "Max number of states")
	sh.write(7, 1, str(maxNos))
	sh.write(8, 0, "Min number of states")
	sh.write(8, 1, str(minNos))
	sh.write(9, 0, "Number of joined states")
	sh.write(9, 1, str(numLinkedStates))
	sh.write(10, 0, "Number of similar states")
	sh.write(10, 1, str(numSimilarStates))
	sh.write(11, 0, "Number of transitions")
	sh.write(11, 1, str(numTransitions))
	sh.write(12, 0, "Number of taken transitions")
	sh.write(12, 1, str(numLiveTransitions))
	sh.write(13, 0, "Number of similar states")
	sh.write(13, 1, str(numDeadTransitions))

	book.save(xlsPath + name + ".xls")

	latexFile = open(resultPath + "transitions/latex_table.txt", "wb")
	latexFile.write("Number of clusters & " + str(noCluster) + ' &\n')
	latexFile.write("Mean number of labels & " + str(meanNol) + ' &\n')
	latexFile.write("Median number of labels & " + str(medianNol) + ' &\n')
	latexFile.write("Max number of labels & " + str(maxNol) + ' &\n')
	latexFile.write("Min number of labels & " + str(minNol) + ' &\n')
	latexFile.write("Mean number of states & " + str(meanNos) + ' &\n')
	latexFile.write("Median number of states & " + str(medianNos) + ' &\n')
	latexFile.write("Max number of states & " + str(maxNos) + ' &\n')
	latexFile.write("Min number of states & " + str(minNos) + ' &\n')
	latexFile.write("Number of joined states & " + str(numLinkedStates) + ' &\n')
	latexFile.write("Number of similar states & " + str(numSimilarStates) + ' &\n')
	latexFile.write("Number of transitions & " + str(numTransitions) + ' &\n')
	latexFile.write("Number of taken transitions & " + str(numLiveTransitions) + ' &\n')
	latexFile.write("Number of untaken transitions & " + str(numDeadTransitions) + ' &\n')

	latexFile.close()

cluster()