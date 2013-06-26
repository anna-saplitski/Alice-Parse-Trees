from node import Node

"""
Do_Together_Node
	-> self.list -- list of nodes in the do DoTogether
"""

class Do_Together_Node( Node ): 
	def __init__(self): 
		Node.__init__(self)
		self.list = []
		self.type = "DoTogether"

	"""
	prints the child nodes
	"""

	def print_children(self, indent_level): 
		for item in self.list: 
			item.print_node(indent_level + 1)

	
	"""
		Inserts a node into the underlying list that Do_Together is represented by. 
	"""
	# child is a Node
	def insert_into_list(self, child): 
		self.list.append(child)

"""
Do_In_Order_Node
	-> self.left_child and self.right_child -- as per usual, contain the sequence of actions in
	the Do_In_Order
"""

class Do_In_Order_Node( Node ): 
	def __init__(self):  
		Node.__init__(self)
		self.type = "DoInOrder"

	def print_children(self, indent_level): 
		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1)
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1)