import sys
import difflib
import collections
import re
import math
import os
import numpy
import array
import Pycluster
import shutil
from sklearn.cluster import AffinityPropagation
from random import randint

def stringDiffComparison(fname1, fname2):
	with open(fname1, "r") as fh1:
		with open(fname2, "r") as fh2:
			differ = difflib.Differ()
			return len(list(differ.compare(fh1.read(), fh2.read())))


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

def automaticComparison(fname1, fname2):
	stringDiffScore = 0
	bagWordScore = 0
	apiCallScore = 0
	astSimilarityScore = 0
#	stringDiffScore = stringDiffComparison(fname1, fname2)	
	bagWordScore = bagWordComparison(fname1, fname2)
	apiCallScore = apiCallComparison(fname1, fname2)
	# astSimilarityScore = astSimilarityComparison(fname1, fname2)
	totalScore = stringDiffScore + 18 * bagWordScore + 270 * apiCallScore + astSimilarityScore
	totalScore = totalScore / 4000
	return totalScore
	
	
	# print "Diff score was: " + str(stringDiffScore)
	# print "Bag score was: " + str(bagWordScore)
	# print "API score was: " + str(apiCallScore)
	# print "AST score was: " + str(astSimilarityScore)
	# print ""
	# print "For a total score of: " + str(totalScore)
	
	# with open(fname1, "r") as fh1:
			# with open(fname2, "r") as fh2:
				# pass
				
def kmeans(folder):
	if folder[-1] != '/':
		folder = folder + '/'
	files = []
	for assignment in os.listdir (folder):
		notUsed, fileExtension = os.path.splitext(assignment)
		if fileExtension == ".txt":
			files.append(assignment)
	randFiles = []
	print "List constructed"
	for i in range(0, 15):
		randFiles.append(files[randint(0, len(files)-1)])
		
	l = len(randFiles)
	distances = []
	print "Random list constructed"
	
	m = [[1 for i in range(l)] for j in range(l)]
	
	for i in range(l):
		for j in range(i+1, l):
			sim = math.exp(-automaticComparison(folder + randFiles[i], folder + randFiles[j]))
			if sim > 0.3:
				m[i][j] = sim
				m[j][i] = sim
			else:
				m[i][j] = 0
				m[j][i] = 0



#	for i in range(l):
#		for j in range(i+1, l):
#			distances.append(automaticComparison(folder + randFiles[i], folder + randFiles[j]))
#
	print "Distances calculated"
	print "Max distance: " + str(max(max(m)))
	print "Avarage distance: " + str(numpy.mean(m))
#	X = 3000
#	Y = 5000
#	Z = 7000
#	W = 10000
#	underX = 0
#	underY = 0
#	underZ = 0
#	underW = 0
#	overW = 0
#	for distance in distances:
#		if distance < X:
#			underX += 1
#		elif distance < Y:
#			underY += 1
#		elif distance < Z:
#			underZ += 1
#		elif distance < W:
#			underW += 1
#		else:
#			overW += 1
#	print "Distances under " + str(X) + ": " + str(underX)
#	print "Distances over " + str(X) + ", under " + str(Y) + ": " + str(underY)
#	print "Distances over " + str(Y) + ", under " + str(Z) + ": " + str(underZ)
#	print "Distances over " + str(Z) + ", under " + str(W) + ": " + str(underW)
#	print "Distances over " + str(W) + ": " + str(overW)
#
#	a = numpy.array(distances, float)
	a = numpy.array(m, float)
	print "Array constructed"
#	labels, error, nfound = Pycluster.kmedoids(distances, 8, 5)
#	print "K-medoids run"

	af = AffinityPropagation(affinity = 'precomputed').fit(a)
	print "Affinity propagation run"

	labels = af.labels_


	resultPath = "/Users/Johan/Documents/AliceResults/"
	
	if os.path.exists(resultPath):
		shutil.rmtree(resultPath)
	os.makedirs(resultPath)
	os.makedirs(resultPath + "labels")
	
	for label in labels:
		if not os.path.exists(resultPath + str(label)):
			shutil.copyfile(folder + randFiles[label], resultPath + "labels" + '/' + randFiles[label])
			os.makedirs(resultPath + str(label))
	
	for i in range(len(randFiles)):
		shutil.copyfile(folder + randFiles[i], resultPath + str(labels[i]) + '/' + randFiles[i])
		
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
	kmeans("/Users/Johan/Documents/AliceData/2_4/")
	# print automaticComparison("C:/cygwin/home/johan/AliceDataCompared/labels/22.16.txt", "C:/cygwin/home/johan/AliceDataCompared/labels/11.20.txt")
else:
    print "Gimme more arguments"