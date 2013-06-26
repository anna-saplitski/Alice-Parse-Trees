from node import Node
from doubles_operators_operations import Double_Node
from calls import Function_Call

"""
Root_Node (the root node for a method or function)
	-> self.return_type -- the return type if there is one. 
	-> self.left_child and self.right_child -- the left and right children. 
"""

class Root_Node ( Node ): 
	def __init__(self):  
		Node.__init__(self)
		self.type = "ROOT"
		self.return_type = None

	"""
	prints the children nodes. 
	"""

	def print_children(self, indent_level): 
		if self.return_type is not None: 
			print 'RETURN TYPE:', self.return_type
		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1, "(ROOT L)")
		else: 
			print "NULL"
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1, "(ROOT R)")

	def is_root(self): 
		return True

	"""
	Gets the node print name for the sake of printing it out. 
	"""

	def get_print_name_for_node(self): 
		if self.name is not None: 
			return self.type + '(' + self.name + ')'
		else: 
			return self.type

	# sets the method name. 
	def set_method_name(self, name): 
		self.name = name

	# sets the return type. 
	def set_return_type(self, t): 
		self.return_type = t

"""
Option1_Node (node type for Move, Roll, Turn)
	-> self.direction -- the direction of the action. 
	-> self.subject -- the subject
	-> self.duration -- the duration (right now, defaults to 1.0)
	-> self.amount -- if the amount is a hardcoded value, then this is an int 
	containing the amount value.
	-> self.left_child -- if the amount is the result of a Function_Call, then
	self.left_child contains the corresponding Function_Call
"""

class Option1_Node( Node ): 
	def __init__(self, t, direc, am, subj, dur = 1.0):  
		Node.__init__(self)
		self.direction = direc
		self.subject = subj
		self.duration = dur
		self.type = t
		
		# tries to see if am is a valid int value. If not, then assumes it 
		# is a function call. 
		try: 
			self.amount = int(am)
		except ValueError: 
			# function name
			self.left_child = Function_Call(am, None)

	# prints the child nodes. 
	def print_children(self, indent_level): 
		if self.left_child is None: 
			print "Type = " + self.type + ", Direction = " + self.direction + ", Subject = " + self.subject + ", Duration = " + str(self.duration) + ", Amount = " + str(self.amount)
		else: 
			print "Type = " + self.type + ", Direction = " + self.direction + ", Subject = " + self.subject + ", Duration = " + str(self.duration) + ", Amount = ",
			self.left_child.print_node(indent_level+1)
	
"""
	Sequence (node type for a sequence of actions)
		-> self.left_child and self.right_child -- contains the actions as per usual. 
"""		
class Sequence( Node ): 
	def __init__(self): 
		Node.__init__(self)
		self.type = "Sequence"

	def print_children(self, indent_level): 
		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1, "(L)")
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1, "(R)")

