from node import Node 
import sys
methods = dict() # maps method names (strings) to their root node

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
		curr_meth = None
		try:
			curr_meth = methods[self.called_name]
		except KeyError:
			pass
		
		output = self.called_name
		for param in self.parameters: 
			output += ' param:' + param
		print output
		if curr_meth is not None:
			curr_meth.print_node(indent_level)
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
