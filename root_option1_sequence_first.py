from node import Node
from doubles_operators_operations import Double_Node
from calls import Function_Call

class Root_Node ( Node ): 
	def __init__(self):  
		Node.__init__(self)
		self.type = "ROOT"
		self.return_type = None

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

	def get_print_name_for_node(self): 
		if self.name is not None: 
			return self.type + '(' + self.name + ')'
		else: 
			return self.type
	def set_method_name(self, name): 
		self.name = name
	def set_return_type(self, t): 
		self.return_type = t

class Option1_Node( Node ): 
	## LOOK UP SPECIFICS
	def __init__(self, t, direc, am, subj, dur = 1.0):  
		Node.__init__(self)
		self.direction = direc
		self.subject = subj
		self.duration = dur
		self.type = t
		#self.amount = am
		
		try: 
			self.amount = int(am)
		except ValueError: 
			# function name
			self.left_child = Function_Call(am, None)

	def print_children(self, indent_level): 
		if self.left_child is None: 
			print "Type = " + self.type + ", Direction = " + self.direction + ", Subject = " + self.subject + ", Duration = " + str(self.duration) + ", Amount = " + str(self.amount)
		else: 
			print "Type = " + self.type + ", Direction = " + self.direction + ", Subject = " + self.subject + ", Duration = " + str(self.duration) + ", Amount = ",
			self.left_child.print_node(indent_level+1)
			
class Sequence( Node ): 
	def __init__(self): 
		Node.__init__(self)
		self.type = "Sequence"

	def print_children(self, indent_level): 
		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1, "(L)")
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1, "(R)")

