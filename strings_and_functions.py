from node import Node 
from doubles_operators_operations import Double_Node

"""
String_Node (node containing string values)
	-> self.value - contains the string value itself. 
"""
class String_Node( Node ): 
	# str is a string
	def __init__(self, str): 
		Node.__init__(self)
		self.value = str
	# prints the value
	def print_children(self, indent_level): 
		print "Value = " + value,

""" 
Simple_Function1 (represents IsFarFrom and IsCloseTo)
	-> self.subject -- the subject. 
	-> self.object -- the object (what we are comparing to)
	-> self.threshold -- the threshold. 
"""
class Simple_Function1( Node ):   
	# tp, s, o are strings. t is a double
	def __init__(self, tp, s, o, t):  
		Node.__init__(self)
		self.type = tp
		self.subject = s
		self.object = o
		self.threshold = t

	# prints the child nodes. 
	def print_children(self, indent_level): 
		print "Type = " + self.type + ", Subject = " + self.subject + ", Object = " + self.object + ", Threshold = " + self.threshold,

"""
Simple_Function2 (node representing DistanceTo)
	-> self.subject -- the subject
	-> self.object -- the object. 
"""
class Simple_Function2( Node ): 
	# tp, s, o are all strings
	def __init__(self, tp, s, o): 
		Node.__init__(self)
		self.type = tp
		self.subject = s
		self.object = o

	def print_children(self, indent_level): 
		print "Type = " + self.type + ", Subject = " + self.subject + ", Object = " + self.object,

"""
Complex_Function -- node representing complex functions. Possibilities are: <, <=, ==, >. >=
e.g X < Y where X and Y can be functions themselves. 
	-> self.type -- string e.g "<"
	-> self.left_child -- the left hand side. 
	-> self.right_child -- the right hand side. can be nested. 
"""

class Complex_Function( Node ): 

	#tp is a string, first and second are Double_Node
	def __init__(self, tp, first=None, second=None):  
		Node.__init__(self)
		self.type = tp
		if first is not None: 
			self.set_left_child(first)
		if second is not None: 
			self.set_right_child(second)

	def print_children(self, indent_level): 
		if self.left_child is not None: 
			self.left_child.print_node(indent_level + 1, "(L)")
		if self.right_child is not None: 
			self.right_child.print_node(indent_level + 1, "(R)")

"""
Represents true values. 
"""
class True_Node(Node): 
	def __init__(self): 
		Node.__init__(self)
		self.type = 'Boolean'
	def print_children(self, indent_level): 
		print 'Value = TRUE',

"""
Represents false values. 
"""
class False_Node(Node): 
	def __init__(self): 
		Node.__init__(self)
		self.type = 'Boolean'
	def print_children(self, indent_level): 
		print 'Value = FALSE',
