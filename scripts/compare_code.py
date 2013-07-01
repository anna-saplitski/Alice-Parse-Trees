import os
from Tkinter import *

class Window():
	def __init__(self):
		self.curr = 0			
		self.root = Tk()
		
		self.fs = FileSelector()
		
		self.frame1 = Frame(self.root,borderwidth=2,relief=SUNKEN)
		self.frame2 = Frame(self.root,borderwidth=2,relief=SUNKEN)
		self.frame3 = Frame(self.root,borderwidth=2,relief=SUNKEN)
		
		self.scroll1 = Scrollbar(self.frame1, orient="vertical")
		self.text1 = Text(self.frame1, wrap=WORD, yscrollcommand=self.scroll1.set)
		self.scroll1.config(command=self.text1.yview)
		self.text1.pack(side=LEFT)
		self.scroll1.pack(side=LEFT, fill=Y)
		self.frame1.grid(row=0)
		
		self.scroll2 = Scrollbar(self.frame2, orient="vertical")
		self.text2 = Text(self.frame2, wrap=WORD, yscrollcommand=self.scroll2.set)
		self.scroll2.config(command=self.text2.yview)
		self.text2.pack(side=LEFT)
		self.scroll2.pack(side=LEFT, fill=Y)
		self.frame2.grid(row=0, column=1)
		
		
		self.question = Label(self.root, text="Are these two code pieces functionally the same?")
		self.question.grid(row=1, columnspan=2)
		
		def wasSimilar():
			self.fs.similar = True
			self.fs.updateFiles()
			self.addCodePages(self.fs.file1, self.fs.file2)
			
		self.yesb = Button(self.root, text="YES", command=wasSimilar)
		self.yesb.pack(side=RIGHT)
		self.yesb.grid(row=2, column=0)
		
		def wasNotSimilar():
			self.fs.similar = False
			self.fs.updateFiles()
			self.addCodePages(self.fs.file1, self.fs.file2)
		
		self.nob = Button(self.root, text="NO", command=wasNotSimilar)
		self.nob.pack(side=LEFT)
		self.nob.grid(row=2, column=1)
		
		self.root.title("Hello")
		self.addCodePages(self.fs.file1, self.fs.file2)
		self.root.mainloop()
	
	def addCodePages(self, fname1, fname2):	
		with open(fname1, "r") as fh1:
			with open(fname2, "r") as fh2:
				content1 = fh1.read()
				content2 = fh2.read()
				self.text1.delete(1.0, END)
				self.text1.insert(INSERT, content1)
				self.text2.delete(1.0, END)
				self.text2.insert(INSERT, content2)	
		self.curr += 1
	

class FileSelector():
	def __init__(self):
		self.file1 = "C:/Documents and Settings/Johan/Documents/GitHub/Alice-Parse-Trees/tests/49.txt"
		self.file2 = "C:/Documents and Settings/Johan/Documents/GitHub/Alice-Parse-Trees/tests/249.txt"
		self.similar = False
		
	def updateFiles(self):
		if self.similar:
			pass
		else:
			pass
		
win = Window()