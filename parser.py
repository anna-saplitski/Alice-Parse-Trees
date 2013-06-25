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

#root = Root_Node() # initial root
parents = Stack() 
nesting = Nesting() # nesting.top() contains the remaining number of non &nbsp
# left to parse in the current level of nesting
methods = dict()
functions = dict()

def parser(): 
	#print "HELLO"
	if len(sys.argv) != 2: 
		print "Usage: Enter one file path to parse"
		return
	html_file = open(sys.argv[1])
	if html_file is None: 
		print "Invalid file name"
		return
		# TODO
	
	content = html_file.read()
	html_file.close()
	content = content.replace('&nbsp', 'nbsp')
	soup = BeautifulSoup(content)
	h2s = soup.find_all('h2')
	#print h2s
	first_methods_table = get_methods_table(soup)
	first_fns_table = get_fns_table(soup)
	"""print '------METHODS TABLE-------'
	print first_methods_table
	print '--------------------------'"""

	tables = soup.find_all('table')
	beginning_methods_counter = -1
	beginning_fns_counter = -1
	for i, t in enumerate(tables): 
		if t == first_methods_table: 
			beginning_methods_counter = i
		if t == first_fns_table: 
			beginning_fns_counter = i

	"""print '---- START TABLE ----'
	print tables[counter]
	print '---------------------'"""

	#print 'NUM TABLES TO DEAL WITH = ', len(tables) - beginning_methods_counter

	# processing the methods
	for i in range(beginning_methods_counter, len(tables)): 

		if i == beginning_fns_counter: 
			break

		method_name = get_method_name(tables[i])
		"""print 'METHOD NAME = ', method_name
		print '------ CURR TABLE ----------'
		print tables[i]
		print '----------------------------'"""
		root = Root_Node()
		initialize_method(root, method_name)
	
		tds = tables[i].find_all('td')
		initialize_tree(tds[1], root)

		"""print '----ALL TDS from tables[i]-------'
		print tables[i].find_all('td')
		print '------------------'

		print '----- TDS from 2 onwards --------'
		for i in range(2, len(tds)): 
			print tds[i]
		print '-------------------'"""

		for j in range(2, len(tds)): 
			"""print '*&*&*&*'
			print tds[i]
			print '*&*------&*&*'"""
			#print tds[i].find_all('b')
			bs = tds[j].find_all('b')

			"""for b in bs: 
				print b.get_text()"""

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
			"""print '\n----BEFORE METHOD CALL ------'
			print_methods()
			print '\n-----XXXXXXXXXXXXXXXX---------'"""
			process_method_call(tds[j])
			if process_nested_filler(tds[j]) == False: 
				nesting.subtract_one()

		#root.print_node(0)

		"""print '*\n*\n*\nALL METHODS DICT '
		print methods
		print '-------------'"""

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
			#print parents.list
			#print nesting.list
			print '------ CURR TABLE ----------'
			print tables[i]
			print '----------------------------'
			for j in range(2, len(tds)): 
				"""print '**** FUNCS  ******'
				print_functions()
				print '********************'
				print '*** CURR TD ******''
				print tds[j]
				print '****************'"""
				#print parents.list
				#print nesting.list
				if nesting.top() == 0: 
					nesting.pop()
					if parents.top() != root: 
						parents.pop()
				#print parents.list
				#print nesting.list
				process_return_stmt(tds[j])
				if process_nested_filler(tds[j]) == False: 
					nesting.subtract_one()
			print '### @@@@@@@@ ######'
			print h2s[1]
			print h2s[1].next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')
			print '### @@@@@@@@ ######'

	# checks return stmts in all functions and if they
	# are returning a string, checks to see if that string
	# is a fn name. if yes, then replace the string w/ a
	# fn call
	replace_strings_with_fn_calls() 

	#print '%%%%^^^^%%%%%'
	print_methods()
	print_functions()
	#print '\n%%%%^^^^%%%%%'

def process_methods(tables, start_index, end_index): 
	pass

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
	tokens = get_b_tokens(td)
	tokens = [str(t) for t in tokens]
	#print tokens
	#print len(tokens)
	if len(tokens) > 1 and 'Return' in tokens[0]:

		try: 
			var = float(tokens[1])
			
		except ValueError:  
			var = tokens[1]
		ret = Return_Node(var)

		insert_into_tree(parents.top(), ret)


def initialize_fn(root, fn_name): 
	functions[fn_name] = root
	parents = Stack()
	nesting = Nesting()


def initialize_method(root, method_name): 
	methods[method_name] = root
	parents = Stack()
	nesting = Nesting()

def get_method_name(table): 
	bs = table.find_all('b')
	return bs[0].get_text()

def get_function_type(table): 
	tds = table.find_all('td')
	text = tds[0].get_text()
	index = text.find(' ')
	return text[10:index]

def print_methods(): 
	print '\nMETHODS'
	for curr_name in methods: 
		#print '\nname = ', curr_name, '\n'
		methods[curr_name].set_method_name(curr_name)
		methods[curr_name].print_node(0)
		print '\n'

def print_functions(): 
	print '\nFUNCTIONS'
	for curr_name in functions: 
		#print '\nname = ', curr_name, '\n'
		functions[curr_name].set_method_name(curr_name)
		functions[curr_name].print_node(0)
		print '\n'

def process_method_call(td): 
	tokens = get_b_tokens(td)
	"""print 'TD = ', td
	print 'TOKENS = ', tokens"""
	if len(tokens) == 1 and tokens[0].find('.') != -1: 
		curr_node = Method_Call(tokens[0], None)
		insert_into_tree(parents.top(), curr_node)
		#print 'INSERTED METHOD CALL: name = ', tokens[0], 'parent = ', parents.top()



def process_operators_from_tokens(tokens, num): 
	"""print 'INITIAL OPERATORS CALL'
	print tokens
	print 'NUM = ', num"""

	if process_double_node_from_tokens(tokens) is True: 
		return
	for i, token in enumerate(tokens): 
		if '*' in token or '/' in token or '+' in token or '-' in token: 

			op = Operator(token.strip())
			operation = Operation(op)
			insert_into_tree(parents.top(), operation)
			parents.push(operation)

			print '\n'
			print 'LEFT LIST'
			print tokens[0:i]
			print 'RIGHT LIST'
			print tokens[i+1:len(tokens)]
			print '\n'
			
			print 'PRE LEFT CALL'
			print tokens[0:i]
			print 'NUM = ', num
			process_operators_from_tokens(tokens[0:i], num+1)
			print 'PRE RIGHT CALL'
			print tokens[i+1:len(tokens)]
			print 'NUM = ', num
			process_operators_from_tokens(tokens[i+1:len(tokens)], num+1)

			parents.pop()
			break

def process_complex_fn(td, if_flag, while_flag):

	if if_flag is False and while_flag is False: 
		return False 
	tokens = get_b_tokens(td)
	if while_flag is True: 
		tokens = tokens[1:len(tokens)]
	for i, token in enumerate(tokens):
		if '==' in token or '!=' in token or '<' in token or '<=' in token \
		or '>' in token or '>=' in token: 
			curr_node = Complex_Function(token)
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node)
			to_process = [tokens[0:i], tokens[i+1:len(tokens)]]


			print '\nBEFORE'
			print to_process[0]
			print 'AFTER'
			print to_process[1]
			print '\n'


			for p in to_process: 
				process_simple_function2_from_tokens(p)
				process_bool_condition_from_tokens(p)
				print 'IN COMPLEX FN'
				if process_double_node_from_tokens(p) is False: 
					process_operators_from_tokens(p, 0)
			parents.pop()
			return True

	return False

def process_double_node_from_tokens(tokens): 

	result = check_if_double_from_tokens(tokens)
	if result[0] is True: 
		curr_node = Double_Node(result[1])
		print '\nINSERT - DOUBLE PROCESSING\n'
		insert_into_tree(parents.top(), curr_node)
		return True
	return False

def check_if_double_from_tokens(tokens): 

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
	tokens = get_b_tokens(td)
	if len(tokens) == 0: 
		return
	if 'Loop' in tokens[0]: 
		if len(tokens) == 3:
		# assert int(tokens[1]) is an int
			print 'FLOAT'
			print float(tokens[1])
			curr_node = Loop_Node(float(tokens[1]))
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node)
		if len(tokens) >= 8: 
			curr_node = Loop_Node(float(tokens[5]), float(tokens[3]), float(tokens[7]))
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node)

def process_wait(td): 
	tokens = get_b_tokens(td)
	if len(tokens) < 2: 
		return
	if 'Wait' in tokens[0]: 
		print 'HERE'
		# TODO assert tokens[1] is an int
		curr_node = Wait_Node(float(tokens[1]))
		insert_into_tree(parents.top(), curr_node)
		print 'SUCCESS'


def process_while(td): 
	tokens = get_b_tokens(td)
	for token in tokens: 
		if 'While' in token: 
			curr_node = While_Node()
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node)
			return True
	return False

def process_bool_condition(td, if_flag, while_flag): 
	if if_flag is False and while_flag is False:
		return
	tokens = get_b_tokens(td)
	process_bool_condition_from_tokens(tokens)


def process_bool_condition_from_tokens(tokens): 
	for token in tokens: 
		if 'true' in token: 
			curr_node = True_Node()
			insert_into_tree(parents.top(), curr_node)
		if 'false' in token: 
			curr_node = False_Node()
			insert_into_tree(parents.top(), curr_node)


def process_else(td): 
	tokens = get_b_tokens(td)
	for token in tokens: 
		if 'Else' in token: 
			curr_node = Else_Node()
			insert_into_tree(parents.top(), curr_node)
			parents.push(curr_node)

def get_b_tokens(td): 
	bs = td.find_all('b')
	return [b.get_text() for b in bs]

def process_if(td): 
	tokens = get_b_tokens(td)
	for token in tokens: 
		if 'If' in token: 
			#print "GOT IT"
			#if_else = If_Else()
			if_node = If_Node()
			#insert_into_tree(if_else, if_node)
			#insert_into_tree(parents.top(), if_else)
			insert_into_tree(parents.top(), if_node)
			parents.push(if_node)
			return True

def process_simple_function2(td): 
	bs = td.find_all('b')
	tokens = [b.get_text() for b in bs]
	process_simple_function2_from_tokens(tokens)


def process_simple_function2_from_tokens(tokens): 
	for i, b in enumerate(tokens): 
		if 'distance to' in b:
			if len(tokens) >= 3 and i < len(tokens) - 1: 
				curr_node = Simple_Function2('DistanceTo', tokens[i-1], tokens[i+1])
				insert_into_tree(parents.top(), curr_node)

def process_simple_function1(td): 
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
	if td.get_text().replace('nbsp;', '') == '': 
		nesting.push(int(td['rowspan']))
		return True
	return False

def initialize_tree(td, root): 
	d = Do_In_Order_Node()
	insert_into_tree(root, d)
	parents.push(root)
	parents.push(d)
	nesting.push(int(td['rowspan']))

# returns the top element on the given stack
def top(stack): 
	if len(stack) >= 1: 
		return stack[len(stack)-1]
	print "Error: Empty stack"
	return None

def process_do_together(td): 
	if "Do together" in td.get_text():
		curr_node = Do_Together_Node()
		insert_into_tree(parents.top(), curr_node)
		parents.push(curr_node)
		

# if td is a basic method, does the needful and returns True
# else returns False
def process_basic_method(td): 
	bs = td.find_all('b')
	tokens = [b.get_text() for b in bs]
	if len(tokens) >= 2:
		if 'move' in tokens[1] or 'roll' in tokens[1] or 'turn' in tokens[1]: 
			curr_node = Option1_Node(option1_get_type(tokens[1]), tokens[2], tokens[3], tokens[0])
			insert_into_tree(parents.top(), curr_node)
			#print 'INSERTING OPTION1 into ', parents.list[0].get_print_name_for_node()
			return True
	return False


def insert_into_do_together(root, child): 
	root.insert_into_list(child)

def insert_into_for_each_together(root, child): 
	return
	# TODO

# root and child are both nodes
def insert_into_tree(root, child): 

	"""print 'ROOT'
	print root
	print 'CHILD'
	print child"""
	try: 
		print child.value
	except: 
		pass

	assert(root is not None)
	if root.get_type() == 'DoTogether': 
		insert_into_do_together(root, child)
		return
	if root.get_type() == 'ForEachTogether': 
		insert_into_for_each_together(root, child)
		return
	if root.get_left_child() is None: 
		root.set_left_child(child)
		return
	curr_right = root.get_right_child()
	if curr_right is None: 
		root.set_right_child(child)
	else: 
		if curr_right.get_type() != 'Sequence':
			seq = Sequence()
			seq.set_left_child(curr_right)
			seq.set_right_child(child)
			child.set_parent(seq)
			root.set_right_child(seq)
			curr_right.set_parent(seq)
			seq.set_parent(root)
		else: 
			insert_into_tree(curr_right, child)

# for an Option1_Node
def option1_get_type(str): 
	if 'move' in str:
		return 'MoveAnimation'
	if 'roll' in str:
		return 'RollAnimation'
	if 'turn' in str: 
		return 'TurnAnimation'

# returns the methods table HTML
def get_methods_table(soup): 
	h3s = soup.find_all('h3')
	for node in h3s: 
		if node.get_text() == "Methods": 
			methods = node
			break
	methods_table = methods.next_sibling.next_sibling # the methods table
	"""print '----'
	print 'METHODS TABLE'
	print methods_table
	print '----'"""
	return methods_table

def get_fns_table(soup): 
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

 
