from node import Node 

class Call( Node ): 
	# name is a string, points_to is a Node
	"""
		Call (the parent class - never used directly)
		-> self.called_name -- the name of the method/function being called. 
		-> self.left_child -- the root of the method or function that has been called.
		-> self.parameters -- list of arguments. 
	"""
	def __init__(self, name, points_to): 
		Node.__init__(self)
		self.called_name = name
		self.left_child = points_to
		self.parameters = [] # list

	# p is a Node
	def insert_parameter(self, p): 
		self.parameters.append(p)

	"""
	prints the child nodes
	"""
	def print_children(self, indent_level): 
		print(self.called_method_name)
		for param in self.parameters: 
			param.print_node(indent_level + 1)
"""
Represents a method call. 
"""

class Method_Call ( Call ): 
	def __init__(self, name, points_to): 
		Call.__init__(self, name, points_to)
		self.type = "MethodCall"

"""
Represents a function call. 
"""
class Function_Call ( Call ): 
	def __init__(self, name, points_to):  	
		Call.__init__(self, name, points_to)
		self.type = "FunctionCall"