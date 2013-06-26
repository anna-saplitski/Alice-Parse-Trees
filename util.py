"""
2 data structures, for convenience. The Stack is a conventional stack built with
an underlying array. The Nesting is a Stack with a built in method that decreases 
each element in its array by 1. It is used for keeping track of spacing. 
"""

class Stack: 
	def __init__(self): 
		self.list = []

	def push(self, item): 
		self.list.append(item)

	def pop(self): 
		return self.list.pop()

	def top(self): 
		if len(self.list) >= 1: 
			return self.list[len(self.list)-1]
		print "Error: Empty stack"
		return None

class Nesting(Stack): 
	def __init__(self): 
		Stack.__init__(self)

	def subtract_one(self): 
		for i, n in enumerate(self.list):
			self.list[i] = n-1
