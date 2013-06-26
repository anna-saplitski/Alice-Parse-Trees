from node import Node
from doubles_operators_operations import Double_Node

"""
Represents wait statements. 

Wait_Node
	-> self.duration -- represents the duration of the wait time.

"""
class Wait_Node ( Node ): 
	# d is a double
	def __init__(self, d): 
		Node.__init__(self)
		self.duration = Double_Node(d)
		self.type = 'Wait'
		assert(self.duration is not None)

	def print_children(self, indent_level): 
		self.duration.print_node(indent_level + 1, "(DURATION)")

"""
Represents loops (i.e Loop 5 times). 
"""
class Loop_Node ( Node ): 
	# all doubles
	"""
	Loop_Node
		-> self.start -- represents the starting number (default is 0.0)
		-> self.end -- represents the end number
		-> self.increment -- represents the increment (default is 1.0)
		-> self.left_child -- as per usual, for the actions associated with the loop
		-> self.right_child -- same as above
	"""
	def __init__(self, e, s=0.0, i=1.0):
		Node.__init__(self)
		self.type = "LoopNInOrder"
		self.start = Double_Node(s)
		self.end = Double_Node(e)
		self.increment = Double_Node(i)
	"""
	prints the child nodes
	"""

	def print_children(self, indent_level): 
		self.start.print_node(indent_level + 1, "(START)")
		self.end.print_node(indent_level + 1, "(END)")
		self.increment.print_node(indent_level + 1, "(INCREMENT)")

		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1, "(ACTIONS)")
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1)

"""
Represents while loops. 
"""
class While_Node ( Node ):

	"""
	While_Node
		-> self.left_child -- condition
		-> self.right_child -- sequence of actions
	"""

	def __init__(self): 
		Node.__init__(self)
		self.type = 'WhileLoopInOrder'

	"""
	prints the child nodes
	"""

	def print_children(self, indent_level):  
		if self.left_child is not None: 
			self.left_child.print_node(indent_level+1, '(CONDITION)')
		if self.right_child is not None: 
			self.right_child.print_node(indent_level+1, '(ACTIONS)')