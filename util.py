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
