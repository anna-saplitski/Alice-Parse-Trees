import os
from Tkinter import *
import threading
import time

class Window(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)	
		self.start()
		
	def callback(self):
		self.root.quit()
		
	def run(self):
		self.curr = 0			
		self.root = Tk()
		
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
		self.question.grid(row=1)
		
		def callback():
			self.curr +=1
			print self.curr
			
		self.b = Button(self.root, text="OK", command=callback)
		self.b.grid(row=1, column=1)

		self.root.title("Hello")
		self.root.mainloop()
	
	def addCodePages(self, fname1, fname2):	
		print "hello"
		with open(fname1, "r") as fh1:
			with open(fname2, "r") as fh2:
				content1 = fh1.read()
				content2 = fh2.read()
				self.text1.delete(1.0, END)
				self.text1.insert(INSERT, content1)
				self.text2.delete(1.0, END)
				self.text2.insert(INSERT, content2)	
		self.curr += 1
	
		
		
win = Window()
time.sleep(.5)
win.addCodePages("C:/Documents and Settings/Johan/Documents/GitHub/Alice-Parse-Trees/tests/49.txt",	"C:/Documents and Settings/Johan/Documents/GitHub/Alice-Parse-Trees/tests/249.txt")