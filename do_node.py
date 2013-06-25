from node import Node

class Do_Together_Node( Node ): 
	def __init__(self): 
		Node.__init__(self)
		self.list = []
		self.type = "DoTogether"

	def print_children(self, indent_level): 
		for item in self.list: 
			item.print_node(indent_level + 1)

	# child is a Node
	def insert_into_list(self, child): 
		self.list.append(child)

class Do_In_Order_Node( Node ): 
	def __init__(self):  
		Node.__init__(self)
		self.type = "DoInOrder"

	def print_children(self, indent_level): 
		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1)
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1)