import sys
import os

basePathWin = "C:\cygwin\home\Johan\AliceData"
basePath = "/home/Johan/AliceData/"
targetPath = "/home/Johan/AliceDataFlattened/"
idnrs = {}
idnr= 0

def a6(id, namePath):
	print "a6"
	
def a7(id, namePath):
	print "a7"
	
def a8(id, namePath):
	print "a8"
	
def l213(id, namePath):
	print "l213"
	
def l215(id, namePath):
	print "l215"
	
def l220(id, namePath):
	print "l220"
	
def l222(id, namePath):
	print "l222"
	
def l225(id, namePath):
	print "l225"
	
def l227(id, namePath):
	print "l227"
	
def l31(id, namePath):
	print "l31"

def l34(id, namePath):
	print "l34"
	
def l36(id, namePath):
	print "l36"

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
						if assignment == "Assignment__6___Introduction_to_Alice_all_files":
							a6(id, namePath)
						elif assignment == "Assignment_7___Programming_in_Alice_all_files":
							a7(id, namePath)
						elif assignment == "Assignment_8a__More_programming_in_Alice_all_files":
							a8(id, namePath)
						elif assignment == "Lab_for_Class_Wednesday_2_13_all_files":
							l213(id, namePath)
						elif assignment == "Lab_for_Class_Friday_2_15_all_files":
							l215(id, namePath)
						elif assignment == "Lab_for_class_Wednesday_2_20_all_files":
							l220(id, namePath)
						elif assignment == "Lab_for_class_Friday_2_22_all_files":
							l222(id, namePath)
						elif assignment == "Lab_for_class_Monday_2_25_all_files":
							l225(id, namePath)
						elif assignment == "Lab_for_Class_Wednesday_2_27_all_files":
							l227(id, namePath)
						elif assignment == "Lab_for_class_Friday_3_1_all_files":
							l31(id, namePath)
						elif assignment == "Lab_for_class_3_4_all_files":
							l34(id, namePath)
						elif assignment == "Lab_for_Class_3_6_all_files":
							l36(id, namePath)
					
