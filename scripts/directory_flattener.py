import sys
import os
import shutil
		
	
COMBOLOCKTASK = "7_4/"
CHECKCANDYTASK = "4/"
SLAPPYTASK = "5_15/"
FROGLADYBUGTASK = "7_5/"
SNOWMOBILETASK = "13/"
FUNKYCHICKENTASK = "14/"
FROGESCAPETASK = "15/"
SNOWPEOPLETASK = "1_3/"
SOLDIERTASK = "1_5/"
CIRCLINGFISHTASK = "2_4/"
TORTOISETASK = "2_5/"

EMPTYTASK = "0/"
JUMPINGCHICKENTASK = "5/"
BURGLARTASK = "6/"
ROVERTASK = "7/"
THREEFROGTASK = "8/"
DANCINGBUNNYTASK = "9/"
CHESIRECATTASK = "10/"
CARTASK = "11/"
BUNNYFLIPPINGTASK = "12/"

basePathWin = "C:\cygwin\home\Johan\AliceData"
basePath = "/home/Johan/AliceData/"
targetPath = "/home/Johan/AliceDataFlattened/"
idnrs = {}
idnr= 0

def renameFiles(id, task, path):
	for dirpath, dirnames, filenames in os.walk(path):
		for file in filenames:
			filePath = dirpath + '/' + file
			filename, fileExtension = os.path.splitext(file)
			if fileExtension == '.html' and filename.isdigit():
				shutil.copy2(filePath, targetPath + task + '/' + str(id) + '.' + file)

def a6(id, namePath):
	for dirpath, dirnames, filenames in os.walk(namePath):
		dirpath = dirpath + '/'
		if ("1.3" in dirpath or "snow" in dirpath or "Snow" in dirpath or "pile" in dirpath or "Pile" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, COMBOLOCKTASK, dirpath)
		elif ("1.5" in dirpath or "sold" in dirpath or "Sold" in dirpath or "deck" in dirpath or "Deck" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, SOLDIERTASK, dirpath)
		elif ("2.4" in dirpath or "circ" in dirpath or "Circ" in dirpath or "fish" in dirpath or "Fish" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, CIRCLINGFISHTASK, dirpath)
		elif ("2.5" in dirpath or "tort" in dirpath or "Tort" in dirpath or "cook" in dirpath or "Cook" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, TORTOISETASK, dirpath)
	
def a7(id, namePath):
	for dirpath, dirnames, filenames in os.walk(namePath):
		dirpath = dirpath + '/'
		if ("7.4" in dirpath or "comb" in dirpath or "lock" in dirpath or "Lock" in dirpath or "Comb" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, COMBOLOCKTASK, dirpath)
		elif ("funk" in dirpath or "Funk" in dirpath or "Chick" in dirpath or "chick" in dirpath or "dance" in dirpath or "Dance" in dirpath or "cool" in dirpath or "Cool" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, FUNKYCHICKENTASK, dirpath)
		elif ("frog" in dirpath or "Frog" in dirpath or "esc" in dirpath or "Esc" in dirpath or "pond" in dirpath or "Pond" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, FROGESCAPETASK, dirpath)
	
def a8(id, namePath):
	for dirpath, dirnames, filenames in os.walk(namePath):
		dirpath = dirpath + '/'
		if ("7.4" in dirpath or "comb" in dirpath or "lock" in dirpath or "Lock" in dirpath or "Comb" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, COMBOLOCKTASK, dirpath)
		elif ("5" in dirpath or "slappy" in dirpath or "Slappy" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, SLAPPYTASK, dirpath)
		elif ("check" in dirpath or "Check" in dirpath or "candy" in dirpath or "Candy" in dirpath or "touch" in dirpath or "Touch" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, CHECKCANDYTASK, dirpath)
		elif ("frog" in dirpath or "Frog" in dirpath or "lady" in dirpath or "Lady" in dirpath or "bug" in dirpath or "Bug" in dirpath or "7.5" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, FROGLADYBUGTASK, dirpath)
		elif ("Snow" in dirpath or "snow" in dirpath) and dirpath.find("Source Code") >= 0:
			renameFiles(id, SNOWMOBILETASK, dirpath)
		
def l213(id, namePath):
	renameFiles(id, EMPTYTASK, namePath)
	
def l215(id, namePath):
	renameFiles(id, JUMPINGCHICKENTASK, namePath)
	
def l220(id, namePath):
	renameFiles(id, ROVERTASK, namePath)
	
def l222(id, namePath):
	renameFiles(id, THREEFROGTASK, namePath)
	
def l225(id, namePath):
	renameFiles(id, DANCINGBUNNYTASK, namePath)
	
def l227(id, namePath):
	renameFiles(id, BURGLARTASK, namePath)
	
def l31(id, namePath):
	renameFiles(id, CHESIRECATTASK, namePath)

def l34(id, namePath):
	renameFiles(id, CARTASK, namePath)
	
def l36(id, namePath):
	renameFiles(id, BUNNYFLIPPINGTASK, namePath)
		

if not os.path.exists(targetPath + COMBOLOCKTASK):
    os.makedirs(targetPath + COMBOLOCKTASK)
if not os.path.exists(targetPath + CHECKCANDYTASK):
    os.makedirs(targetPath + CHECKCANDYTASK)
if not os.path.exists(targetPath + SLAPPYTASK):
    os.makedirs(targetPath + SLAPPYTASK)
if not os.path.exists(targetPath + FROGLADYBUGTASK):
    os.makedirs(targetPath + FROGLADYBUGTASK)
if not os.path.exists(targetPath + SNOWMOBILETASK):
    os.makedirs(targetPath + SNOWMOBILETASK)
if not os.path.exists(targetPath + FUNKYCHICKENTASK):
    os.makedirs(targetPath + FUNKYCHICKENTASK)
if not os.path.exists(targetPath + FROGESCAPETASK):
    os.makedirs(targetPath + FROGESCAPETASK)
if not os.path.exists(targetPath + SNOWPEOPLETASK):
    os.makedirs(targetPath + SNOWPEOPLETASK)
if not os.path.exists(targetPath + SOLDIERTASK):
    os.makedirs(targetPath + SOLDIERTASK)
if not os.path.exists(targetPath + CIRCLINGFISHTASK):
    os.makedirs(targetPath + CIRCLINGFISHTASK)
if not os.path.exists(targetPath + TORTOISETASK):
    os.makedirs(targetPath + TORTOISETASK)
if not os.path.exists(targetPath + EMPTYTASK):
    os.makedirs(targetPath + EMPTYTASK)
if not os.path.exists(targetPath + JUMPINGCHICKENTASK):
    os.makedirs(targetPath + JUMPINGCHICKENTASK)
if not os.path.exists(targetPath + BURGLARTASK):
    os.makedirs(targetPath + BURGLARTASK)
if not os.path.exists(targetPath + ROVERTASK):
    os.makedirs(targetPath + ROVERTASK)
if not os.path.exists(targetPath + THREEFROGTASK):
    os.makedirs(targetPath + THREEFROGTASK)
if not os.path.exists(targetPath + DANCINGBUNNYTASK):
    os.makedirs(targetPath + DANCINGBUNNYTASK)
if not os.path.exists(targetPath + CHESIRECATTASK):
    os.makedirs(targetPath + CHESIRECATTASK)
if not os.path.exists(targetPath + CARTASK):
    os.makedirs(targetPath + CARTASK)
if not os.path.exists(targetPath + BUNNYFLIPPINGTASK):
    os.makedirs(targetPath + BUNNYFLIPPINGTASK)


	
		
for assignment in os.listdir (sys.argv[1]):
	assignPath = basePath + assignment + '/'
	if os.path.isdir(assignPath):
		for zips in os.listdir(assignPath):
			zipPath = assignPath + zips + '/'
			if os.path.isdir(zipPath):
				for name in os.listdir(zipPath):
					namePath = zipPath + name + '/'
					if os.path.isdir(namePath):
						if name not in idnrs:
							idnrs[name] = idnr
							idnr += 1
						id = idnrs[name]
print idnrs
						# if assignment == "Assignment__6___Introduction_to_Alice_all_files":
							# a6(id, namePath)
						# elif assignment == "Assignment_7___Programming_in_Alice_all_files":
							# a7(id, namePath)
						# elif assignment == "Assignment_8a__More_programming_in_Alice_all_files":
							# a8(id, namePath)
						# elif assignment == "Lab_for_Class_Wednesday_2_13_all_files":
							# l213(id, namePath)
						# elif assignment == "Lab_for_Class_Friday_2_15_all_files":
							# l215(id, namePath)
						# elif assignment == "Lab_for_class_Wednesday_2_20_all_files":
							# l220(id, namePath)
						# elif assignment == "Lab_for_class_Friday_2_22_all_files":
							# l222(id, namePath)
						# elif assignment == "Lab_for_class_Monday_2_25_all_files":
							# l225(id, namePath)
						# elif assignment == "Lab_for_Class_Wednesday_2_27_all_files":
							# l227(id, namePath)
						# elif assignment == "Lab_for_class_Friday_3_1_all_files":
							# l31(id, namePath)
						# elif assignment == "Lab_for_class_3_4_all_files":
							# l34(id, namePath)
						# elif assignment == "Lab_for_Class_3_6_all_files":
							# l36(id, namePath)
					
