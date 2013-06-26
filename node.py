"""
Elements in the AST have various types. Node is the parent class of them all. 
(It is never used directly).
Each Node has a left_child, a right_child, a type, an address, and a name. 

"""

class Node: 
	def __init__(self): 
		self.parent = None
		self.right_child = None
		self.left_child = None
		self.type = ""
		self.address = ""
		self.name = None

	"""
	Various setter and getter methods. 
	"""

	# p is a Node
	def set_parent(self, p): 
		self.parent = p

	def get_parent(self): 
		return self.parent

	def get_type(self): 
		return self.type

	# t is a string
	def set_type(self, t): 
		self.type = t

	# c is a Node
	def set_right_child(self, c): 
		self.right_child = c

	def get_right_child(self): 
		return self.right_child

	def set_left_child(self, c): 
		self.left_child = c

	def get_left_child(self): 
		return self.left_child

	# a is a string
	def set_address(self, a): 
		self.address = a

	def get_address(self): 
		return self.address

	def is_root(self): 
		return false

	def get_print_name_for_node(self): 
		return self.type


	""""
	Recursively prints out the Node's details and then prints those of its children with
	the appropriate spacing determined by the indent_level, with an optional label. 
	print_children(indent_level) is a virtual function that is defined by each Node subclass differently. 
	"""
	# indent_level is an int, label is a string
	def print_node(self, indent_level, label=None):  
		num_spaces = 3
		print '\n',
		print ' ' * num_spaces, 
		print ' ' * (indent_level * num_spaces),

		if label is not None: 
			print label,
		else: 
			print ' ',

		print self.get_print_name_for_node() + ':',

		self.print_children(indent_level)


