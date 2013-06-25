from node import Node

class For_Each_In_Order ( Node ): 
	# l is a string
	def __init__(self, l): 
		self.list_name = l
		self.type = "For_Each_In_Order"

	def print_children(self, indent_level): 
		print "List: " + self.list_name
		if self.left_child != NULL: 
			self.left_child.print_node(indent_level + 1, "(ACTIONS)")
		if self.right_child != NULL: 
			self.right_child.print_node(indent_level + 1)


class For_Each_Together( Node ): 
	def __init__(self, l): 
		self.list_name = l
		self.list = []
		self.type = "ForEachTogether"

	def print_children(self, indent_level): 
		print "List: " + self.list_name

		for item in self.list: 
			item.print_node(indent_level + 1)

	# child is a Node
	def insert_into_list(self, child): 
		self.list.append(child)

class List_Node ( Node ): 
	# n is string, i_n is list of item_names (strings)
	def __init__(self, n, i_n):
		self.type = "List"
		self.name = n
		self.item_names = i_n

	def print_children(self, indent_level): 
		print "List name: " + self.name
		for item in self.item_names: 
			print item

	def insert_name(self, name): 
		self.item_names.append(name)
