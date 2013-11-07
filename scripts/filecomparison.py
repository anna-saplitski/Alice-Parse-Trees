#Belanced coeff = BOW: 1, API: 0.5, SPEC: 6 
stringDiffParam = 0
bagWordParam = 0
apiCallParam = 1
dancingBunnyParam = 0

# Sum all of the comparisons 
def fileComparison(fname1, fname2):
	stringDiffScore = 0
	bagWordScore = 0
	apiCallScore = 0
	dancingBunnyScore = 0
	if stringDiffParam > 0:
		stringDiffScore = stringDiffParam * stringDiffComparison(fname1, fname2)
	if bagWordParam > 0:
		bagWordScore = bagWordParam * bagWordComparison(fname1, fname2)
	if apiCallParam > 0:
		apiCallScore = apiCallParam * apiCallComparison(fname1, fname2)
	if dancingBunnyParam > 0:
		dancingBunnyScore = dancingBunnyParam * dancingBunnyComparison(fname1, fname2)
	totalScore = stringDiffScore + bagWordScore + apiCallScore + dancingBunnyScore
	return totalScore
	
# Run a straight up diff between the two text files, very slow
def stringDiffComparison(fname1, fname2):
	with open(fname1, "r") as fh1:
		with open(fname2, "r") as fh2:
			differ = difflib.Differ()
			return len(list(differ.compare(fh1.read(), fh2.read())))

# Compare the differences in how many times a word appears in each file
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
	
# Check for the Alice API calls move, turn and roll and do a sring DNA comparison between them
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