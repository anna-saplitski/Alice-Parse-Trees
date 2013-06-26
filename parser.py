from node import *
from do_node import Do_Together_Node, Do_In_Order_Node
from if_else import *
from wait_loop_while import Wait_Node, Loop_Node, While_Node
from doubles_operators_operations import *
from calls import *
from vars_and_return import Return_Node

# from lists-for-each import *
from strings_and_functions import String_Node, Simple_Function1, Simple_Function2, Complex_Function
from strings_and_functions import True_Node, False_Node
from root_option1_sequence_first import *
import re, string, sys, os
from bs4 import BeautifulSoup
from util import Stack, Nesting

parents = Stack() 
nesting = Nesting() # nesting.top() contains the remaining number of non &nbsp
# left to parse in the current level of nesting
methods = dict() # maps method names (strings) to their root node
functions = dict() # maps function names (strings) to their root node

def parser(): 
	if len(sys.argv) != 2: 
		print "Usage: Enter one file path to parse"
		return
	try: 
		html_file = open(sys.argv[1])
	except:
		print "Invalid file name. Enter an Alice HTML file name."
		return

	content = html_file.read()
	html_file.close()
	content = content.replace('&nbsp', 'nbsp') # makes it easier to find and keep track
	# of the nbsp's
	soup = BeautifulSoup(content)
	h2s = soup.find_all('h2')
	first_methods_table = get_methods_table(soup) # uses the tree structure to get the methods table
	first_fns_table = get_fns_table(soup) # uses the tree structure to get the functions table. 

	tables = soup.find_all('table')
	beginning_methods_counter = -1
	beginning_fns_counter = -1
	for i, t in enumerate(tables): 
		if t == first_methods_table: 
			beginning_methods_counter = i
		if t == first_fns_table: 
			beginning_fns_counter = i

	# processing the methods
	for i in range(beginning_methods_counter, len(tables)): 

		if i == beginning_fns_counter: 
			break

		method_name = get_method_name(tables[i])
		root = Root_Node()
		initialize_method(root, method_name)
	
		tds = tables[i].find_all('td')
		initialize_tree(tds[1], root)

		for j in range(2, len(tds)): 
			bs = tds[j].find_all('b')

			if nesting.top() == 0: 
				nesting.pop()
				if parents.top() != root: 
					parents.pop()
			if_flag = process_if(tds[j])
			while_flag = process_while(tds[j])
			process_bool_condition(tds[j], if_flag, while_flag)
			if process_complex_fn(tds[j], if_flag, while_flag) is False: 
				process_simple_function1(tds[j])
				process_simple_function2(tds[j])
			process_else(tds[j])
			process_basic_method(tds[j])
			process_loop(tds[j])
			process_do_together(tds[j])
			process_wait(tds[j])


			process_method_call(tds[j])
			"""
			In order to correctly display the levels of scoping, the HTML has a number
			of filler <td> elements to form spaces. e.g 
			<filler>While<condition>
			<filler><filler>ACTION (in while loop)
			<filler>ACTION (outside while loop)
			See process_nested_filler. The td['rowspan'] says how many non-filler elements
			are in a particular scope, so nesting contains the number of non-filler elements
			left to parse in each scope (it's a stack-like structure so LIFO). So if tds[j] is not
			a filler element, then we want to subtract one from each element in nesting. 
			"""
			if process_nested_filler(tds[j]) == False: 
				nesting.subtract_one()

	# processing functions
	if beginning_fns_counter != -1: 
		for i in range(beginning_fns_counter, len(tables)): 
			fn_name = get_method_name(tables[i])
			print 'FN NAME = ', fn_name
			root = Root_Node()
			initialize_fn(root, fn_name)
			tds = tables[i].find_all('td')
			
			initialize_tree(tds[1], root)
			ret_type = get_function_type(tables[i])
			root.set_return_type(ret_type)

			for j in range(2, len(tds)): 
				if nesting.top() == 0: 
					nesting.pop()
					if parents.top() != root: 
						parents.pop()
				process_return_stmt(tds[j])
				"""
				In order to correctly display the levels of scoping, the HTML has a number
				of filler <td> elements to form spaces. e.g 
				<filler>While<condition>
				<filler><filler>ACTION (in while loop)
				<filler>ACTION (outside while loop)
				See process_nested_filler. The td['rowspan'] says how many non-filler elements
				are in a particular scope, so nesting contains the number of non-filler elements
				left to parse in each scope (it's a stack-like structure so LIFO). So if tds[j] is not
				a filler element, then we want to subtract one from each element in nesting. 
				"""
				if process_nested_filler(tds[j]) == False: 
					nesting.subtract_one()

	# checks return stmts in all functions and if they
	# are returning a string, checks to see if that string
	# is a fn name. if yes, then replace the string w/ a
	# fn call
	replace_strings_with_fn_calls() 

	print_methods()
	print_functions()

def process_methods(tables, start_index, end_index): 
	pass

# checks return stmts in all functions and if they
# are returning a string, checks to see if that string
# is a fn name. if yes, then replace the string w/ a
# fn call
def replace_strings_with_fn_calls(): 
	for fn_name in functions:
		fn = functions[fn_name]
		return_node = fn.get_right_child()
		if return_node is not None: 
			string_val = return_node.get_string_value()
			if string_val is not None: 
				if string_val in functions: 
					fn_call = Function_Call(string_val, None)
					return_node.set_left_child(fn_call)

def process_return_stmt(td): 
	"""
	If td is a return statement, then it creates a Return_Node and adds it to the tree. 
	"""
	tokens = get_b_tokens(td)
	tokens = [str(t) for t in tokens]
	if len(tokens) > 1 and 'Return' in tokens[0]:

		try: 
			var = float(tokens[1]) # checks to see if the return value is a float
			
		except ValueError:  
			var = tokens[1] # otherwise, stores it as a string value. 
		ret = Return_Node(var)

		insert_into_tree(parents.top(), ret)


def initialize_fn(root, fn_name): 
	# initializes fn_name in the functions dict and resets parents and nesting. 
	functions[fn_name] = root
	parents = Stack()
	nesting = Nesting()


def initialize_method(root, method_name): 
	# initializes methd_name in the methods dict and resets parents and nesting. 
	methods[method_name] = root
	parents = Stack()
	nesting = Nesting()

def get_method_name(table): 
	# uses the Beautiful Soup tree structure to find and return the method name
	bs = table.find_all('b')
	return bs[0].get_text()

def get_function_type(table): 
	# uses the Beautiful Soup tree structure to find and return the function return type. 
	tds = table.find_all('td')
	text = tds[0].get_text()
	index = text.find(' ')
	return text[10:index]

def print_methods(): 
	# prints all method trees. 
	print '\nMETHODS'
	for curr_name in methods: 
		methods[curr_name].set_method_name(curr_name)
		methods[curr_name].print_node(0)
		print '\n'

def print_functions(): 
	# prints all function trees. 
	print '\nFUNCTIONS'
	for curr_name in functions: 
		functions[curr_name].set_method_name(curr_name)
		functions[curr_name].print_node(0)
		print '\n'

def process_method_call(td): 
	# if td is a method call, then creates a corresponding Method_Call node and adds
	# it to the tree. 
	tokens = get_b_tokens(td)
	if len(tokens) == 1 and tokens[0].find('.') != -1: 
		curr_node = Method_Call(tokens[0], None)
		insert_into_tree(parents.top(), curr_node)

def process_operators_from_tokens(tokens, num): 
	# recursively processes math operations and adds them to the tree. 
	if process_double_node_from_tokens(tokens) is True: 
		return
	for i, token in enumerate(tokens): 
		if '*' in token or '/' in token or '+' in token or '-' in token: 
			op = Operator(token.strip())
			operation = Operation(op) # makes a new Operation of that type. 
			insert_into_tree(parents.top(), operation) # inserts it into the tree. 
			parents.push(operation) # pushes it onto parents so the following recursive calls will
			# add the new doubles or Operations to the right place. 
			process_operators_from_tokens(tokens[0:i], num+1) # processes LHS
			process_operators_from_tokens(tokens[i+1:len(tokens)], num+1) # processes RHS
			parents.pop() # removes the operation
			break

def process_complex_fn(td, if_flag, while_flag):
	# see strings_and_functions.py for more info about complex functions. 
	if if_flag is False and while_flag is False: # must be within an if or a while statement. 
		return False 
	tokens = get_b_tokens(td)
	if while_flag is True: 
		tokens = tokens[1:len(tokens)]
	for i, token in enumerate(tokens):
		if '==' in token or '!=' in token or '<' in token or '<=' in token \
		or '>' in token or '>=' in token: 
			curr_node = Complex_Function(token) # makes a new Complex_Function of that type
			insert_into_tree(parents.top(), curr_node) # adds it to tree
			parents.push(curr_node) # pushes it onto parents so the following code adds new
			# nodes to the right place. 
			to_process = [tokens[0:i], tokens[i+1:len(tokens)]]

			# processes the remaining tokens
			for p in to_process: 
				process_simple_function2_from_tokens(p)
				process_bool_condition_from_tokens(p)
				if process_double_node_from_tokens(p) is False: 
					process_operators_from_tokens(p, 0)
			parents.pop() # removes the complex fn from parents
			return True

	return False

def process_double_node_from_tokens(tokens): 
	# if tokens encodes a double, adds the corresponding Double_Node to the tree. 
	result = check_if_double_from_tokens(tokens)
	if result[0] is True: 
		curr_node = Double_Node(result[1])
		insert_into_tree(parents.top(), curr_node)
		return True
	return False

def check_if_double_from_tokens(tokens): 
	# checks to see if tokens encodes a double. 
	result = []
	for t in tokens: 
		if t != '' and ')' not in t and '(' not in t: 
			result.append(t)
	if len(result) == 1: 
		try: 
			value = float(result[0])
			return (True, value)
		except: 
			pass
	return (False, None)


def process_loop(td): 
	# if td encodes a Loop, processes it. 
	tokens = get_b_tokens(td)
	if len(tokens) == 0: 
		return
	if 'Loop' in tokens[0]: 
		if len(tokens) == 3:
			# default start and increment values
			curr_node = Loop_Node(float(tokens[1]))
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node) # pushes onto tree so the statements in the loop have the 
			# Loop_Node as their parent. 
		if len(tokens) >= 8: 
			# custom start and increment values
			curr_node = Loop_Node(float(tokens[5]), float(tokens[3]), float(tokens[7]))
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node) # pushes onto tree so the statements in the loop have the 
			# Loop_Node as their parent. 

def process_wait(td): 
	# if td encodes a wait statement, creates a corresponding Wait_Node and
	# adds it to the tree. 
	tokens = get_b_tokens(td)
	if len(tokens) < 2: 
		return
	if 'Wait' in tokens[0]: 
		curr_node = Wait_Node(float(tokens[1]))
		insert_into_tree(parents.top(), curr_node)


def process_while(td): 
	# if td encodes a while loop, processes it and adds the While_Node to the tree. 
	tokens = get_b_tokens(td)
	for token in tokens: 
		if 'While' in token: 
			curr_node = While_Node()
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node) # pushes onto parents so the statements in the while loop have the 
			# While_Node as their parent. 
			return True
	return False

def process_bool_condition(td, if_flag, while_flag): 
	if if_flag is False and while_flag is False: # have to be in an if or while statement. 
		return
	tokens = get_b_tokens(td)
	process_bool_condition_from_tokens(tokens)


def process_bool_condition_from_tokens(tokens): 
	# creates a True_Node or False_Node and adds to tree where appropriate. 
	for token in tokens: 
		if 'true' in token: 
			curr_node = True_Node()
			insert_into_tree(parents.top(), curr_node) 
		if 'false' in token: 
			curr_node = False_Node()
			insert_into_tree(parents.top(), curr_node)


def process_else(td): 
	# processes an else statement. 
	tokens = get_b_tokens(td)
	for token in tokens: 
		if 'Else' in token: 
			curr_node = Else_Node()
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node) # pushes onto parents so nodes in the else statement become
			# children of the Else_Node. 

def get_b_tokens(td): 
	# gets all the bold tokens in td (what actually matter)
	bs = td.find_all('b')
	return [b.get_text() for b in bs]

def process_if(td): 
	# if td is an if statement, processes it. 
	tokens = get_b_tokens(td)
	for token in tokens: 
		if 'If' in token: 
			if_node = If_Node()
			insert_into_tree(parents.top(), if_node)
			parents.push(if_node)
			return True

def process_simple_function2(td): 
	# if td is a simple function 2 (i.e DistanceTo), processes it. 
	bs = td.find_all('b')
	tokens = [b.get_text() for b in bs]
	process_simple_function2_from_tokens(tokens)


def process_simple_function2_from_tokens(tokens): 
	# checks to see if tokens encodes a simple function 2 (i.e DistanceTo) and 
	# adds the node to a tree accordingly. 
	for i, b in enumerate(tokens): 
		if 'distance to' in b:
			if len(tokens) >= 3 and i < len(tokens) - 1: 
				curr_node = Simple_Function2('DistanceTo', tokens[i-1], tokens[i+1])
				insert_into_tree(parents.top(), curr_node)

def process_simple_function1(td): 
	# if td is a simple_function1, processes it.
	bs = td.find_all('b')
	if len(bs) <= 1: 
		return
	tokens = [b.get_text() for b in bs[1:len(bs)]]
	if len(tokens) > 1: 
		if 'is within' in tokens[1] or 'is at least' in tokens[1]: 
			assert(len(tokens) > 4)
			curr_node = Simple_Function1(sf1_get_type(tokens[1]), tokens[0], tokens[4], tokens[2])
			insert_into_tree(parents.top(), curr_node)

# returns type for a simple_function1
def sf1_get_type(token): 
	if 'is within' in token:
		return 'IsCloseTo'
	if 'is at least' in token: 
		return 'IsFarFrom'

def process_nested_filler(td): 	
	# if td is a filler element, pushes the number of nonfiller elements onto nesting. 
	if td.get_text().replace('nbsp;', '') == '': 
		nesting.push(int(td['rowspan']))
		return True
	return False

def initialize_tree(td, root): 
	# initializes root, parents, and nesting. 
	d = Do_In_Order_Node()
	insert_into_tree(root, d)
	parents.push(root)
	parents.push(d)
	nesting.push(int(td['rowspan']))

def process_do_together(td): 
	# processes do together if that's what td is
	if "Do together" in td.get_text():
		curr_node = Do_Together_Node()
		insert_into_tree(parents.top(), curr_node)
		parents.push(curr_node)

# if td is a basic method (i.e move, roll, or turn), does the needful and returns True
# else returns False
def process_basic_method(td): 
	bs = td.find_all('b')
	tokens = [b.get_text() for b in bs]
	if len(tokens) >= 2:
		if 'move' in tokens[1] or 'roll' in tokens[1] or 'turn' in tokens[1]: 
			curr_node = Option1_Node(option1_get_type(tokens[1]), tokens[2], tokens[3], tokens[0])
			insert_into_tree(parents.top(), curr_node)
			return True
	return False


def insert_into_do_together(root, child): 
	root.insert_into_list(child)

def insert_into_for_each_together(root, child): 
	return
	# TODO

# root and child are both nodes
def insert_into_tree(root, child): 
	# inserts child into the tree with root as the root
	assert(root is not None)
	if root.get_type() == 'DoTogether': 
		insert_into_do_together(root, child) # inserts into the do together list
		return
	if root.get_type() == 'ForEachTogether': 
		insert_into_for_each_together(root, child) # inserts into the for each together list
		return
	if root.get_left_child() is None: 
		root.set_left_child(child) # inserts into the tree starting from the left child. 
		return
	curr_right = root.get_right_child()
	# if root's right child is None, sets the right child to be child. 
	if curr_right is None: 
		root.set_right_child(child)
	else: 
		""" Sequence nodes indicate a sequence of nodes. e.g if the tree currently looks like this: 
		Do In order
	  /			\
	  Move 		Roll

	  And we want to add Turn to this, then this is what the tree would look like: 

		Do In order
	  /			\
	  Move 		Sequence node
	  			/	\
	  		Roll     Turn

		"""
		if curr_right.get_type() != 'Sequence':
			seq = Sequence()
			seq.set_left_child(curr_right)
			seq.set_right_child(child)
			child.set_parent(seq)
			root.set_right_child(seq)
			curr_right.set_parent(seq)
			seq.set_parent(root)
		else: 
			"""
			E.g if the tree currently looks like this: 
		Do In order
	  /			\
	  Move 		Sequence node
	  			/	\
	  		Roll     Turn

	  and we want to add another Move, then we recursively call insert_into_tree on the tree rooted at
	  Sequence node. The end result would look like this: 

	  	Do In order
	  /			\
	  Move 		Sequence node
	  			/	\
	  		Roll     Sequence
	  				/		\
	  			Turn  		Move


			"""
			insert_into_tree(curr_right, child)

# for an Option1_Node
def option1_get_type(str): 
	if 'move' in str:
		return 'MoveAnimation'
	if 'roll' in str:
		return 'RollAnimation'
	if 'turn' in str: 
		return 'TurnAnimation'

# returns the methods table HTML using the Beautiful Soup tree structure. 
def get_methods_table(soup): 
	h3s = soup.find_all('h3')
	for node in h3s: 
		if node.get_text() == "Methods": 
			methods = node
			break
	methods_table = methods.next_sibling.next_sibling # the methods table
	return methods_table

def get_fns_table(soup): 
	# uses the Beautiful Soup tree structure to find and return the functions table. 
	h3s = soup.find_all('h3')
	fns = None
	for node in h3s: 
		if 'Functions' in node.get_text(): 
			fns = node
			break
	if fns is not None: 
		fns_table = fns.next_sibling.next_sibling # the first fn table
		return fns_table
	return None

def main(): 
  parser()

if __name__ == "__main__": 
  main()

 
