from node import Node 
from doubles_operators_operations import Double_Node

"""
Set_Var_Node -- to set a mutable variable -- not used yet. 
	-> self.property_name -- the property name. 
	-> self.string_value -- the string value, if we are dealing with a string or
	the bool value if it's a bool. 
	-> self.var_name -- the variable name. 
	-> self.left_child -- the double_node value, if it's a double. 
"""

"""
class Set_Var_Node ( Node ): 
	# both strings
	def __init__(self, v, p): 
		self.property_name = p
		self.type = "PropertyAnimation / MutableVariable" 
		#ie mutable variable, but this is what Alice calls it
		self.string_value = "-1"
		self.var_name = v

	# d is double
	def __init__(self, v, p, d):
		self.string_value = "-1"
		self.var_name = v
		self.property_name = p
		self.left_child = Double_Node(d)
		self.type = "SetMutableVariable" # ie according to Alice, a PropertyAnimation

	# is_var is bool
	def __init__(self, v, p, sv, is_var): 
		self.var_name = v
		self.type = "SetMutableVariable"

		if (isVar == False): 
			self.string_value = sv
			self.property_name = p 
		else: 
			self.left_child = Var_Access(sv)

	def print_children(self, indent_level): 
		print "Variable name: " + self.var_name + ", Property name: " + self.property_name
		if (self.left_child != NULL): 
			self.left_child.print_node(indent_level + 1)
		else: 
			if self.string_value = "true" or self.string_value = "false": 
				print ", Bool value: " + self.string_value
			else: 
				print ", String value: " + self.string_value


"""

"""
Var_Access -- represents variable access - unused so far. 
	-> self.var_name -- the variable name. 
"""

"""

class Var_Access ( Node ): 
	def __init__(self, n):
		self.var_name = n
		self.type = "Variable Access"

	def print_children(self, indent_level): 
		print "Variable name = " + var_name
"""

"""
Return_Node -- represents the value returned. 
	-> self.string_value -- contains the return value if a string is being returned.
	-> self.left_child -- if a double is being returned, contains the corresponding
	Double_Node. 
"""
class Return_Node ( Node ): 
	# var is either a double or a string
	def __init__(self, var):  
		Node.__init__(self)
		if isinstance(var, float):
			self.string_value = None
			self.left_child = Double_Node(var)
			self.type = "ReturnStmt"
		else: 
			if isinstance(var, str): 
				self.string_value = var 
				self.type = "ReturnStmt"

	# returns true if a string (other than true or false, which are bools) is being
	# returned. 
	def has_string_value(self): 
		if self.string_value is None: 
			return False
		if self.string_value == 'true' or self.string_value == 'false': 
			return False
		return True

	# returns the string value if it's a string. 
	def get_string_value(self): 
		if self.has_string_value() is True: 
			return self.string_value
		return None

	# prints the child nodes. 
	def print_children(self, indent_level): 
		if self.left_child is not None:
			self.left_child.print_node(indent_level + 1)
		else: 
			if self.string_value == "true" or self.string_value == "false": 
				print "Bool value: " + self.string_value
			else: 
				print "String value: " + self.string_value

