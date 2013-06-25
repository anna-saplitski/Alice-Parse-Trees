from node import Node
from doubles_operators_operations import Double_Node

class Wait_Node ( Node ): 
	# d is a double
	def __init__(self, d): 
		Node.__init__(self)
		self.duration = Double_Node(d)
		self.type = 'Wait'
		assert(self.duration is not None)

	def print_children(self, indent_level): 
		self.duration.print_node(indent_level + 1, "(DURATION)")

class Loop_Node ( Node ): 
	# all doubles
	def __init__(self, e, s=0.0, i=1.0):
		Node.__init__(self)
		self.type = "LoopNInOrder"
		self.start = Double_Node(s)
		self.end = Double_Node(e)
		self.increment = Double_Node(i)

		#assert(self.start is not None and end is not None and increment is not None);  TODO

	def print_children(self, indent_level): 
		self.start.print_node(indent_level + 1, "(START)")
		self.end.print_node(indent_level + 1, "(END)")
		self.increment.print_node(indent_level + 1, "(INCREMENT)")

		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1, "(ACTIONS)")
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1)

class While_Node ( Node ):
	# left_node is the condition
	# right_node is the sequence of actions

	def __init__(self): 
		Node.__init__(self)
		self.type = 'WhileLoopInOrder'
		#   assert (duration is not None); TODO

	def print_children(self, indent_level):  
		if self.left_child is not None: 
			self.left_child.print_node(indent_level+1, '(CONDITION)')
		if self.right_child is not None: 
			self.right_child.print_node(indent_level+1, '(ACTIONS)')