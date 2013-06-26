from node import Node

"""
For_Each_In_Order
	-> self.list_name -- the list name. 
	-> self.left_child and self.right_child -- the actions for the list. 
"""

class For_Each_In_Order ( Node ): 
	# l is a string
	def __init__(self, l): 
		self.list_name = l
		self.type = "For_Each_In_Order"

	"""
	prints the children nodes. 
	"""

	def print_children(self, indent_level): 
		print "List: " + self.list_name
		if self.left_child != NULL: 
			self.left_child.print_node(indent_level + 1, "(ACTIONS)")
		if self.right_child != NULL: 
			self.right_child.print_node(indent_level + 1)

"""
For_Each_Together
	-> self.list_name -- the list name. 
	-> self.list -- the list of actions that must be performed together. 
"""

class For_Each_Together( Node ): 
	def __init__(self, l): 
		self.list_name = l
		self.list = []
		self.type = "ForEachTogether"

	"""
	prints the children nodes. 
	"""

	def print_children(self, indent_level): 
		print "List: " + self.list_name

		for item in self.list: 
			item.print_node(indent_level + 1)

	"""
	Inserts a child node into the list. 
	"""
	# child is a Node
	def insert_into_list(self, child): 
		self.list.append(child)

"""
List_Node
	-> self.name -- list name
	-> self.item_names -- list of the names of the items in the List
"""

class List_Node ( Node ): 
	# n is string, i_n is list of item_names (strings)
	def __init__(self, n, i_n):
		self.type = "List"
		self.name = n
		self.item_names = i_n

	"""
	prints the children nodes. 
	"""

	def print_children(self, indent_level): 
		print "List name: " + self.name
		for item in self.item_names: 
			print item

	"""
	Inserts a name into the list. 
	"""
	def insert_name(self, name): 
		self.item_names.append(name)
