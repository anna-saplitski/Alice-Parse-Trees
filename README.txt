This is a parser to build ASTs out of HTML files of Alice programs. It uses Beautiful Soup, an HTML parser in Python, that you can download here: http://www.crummy.com/software/BeautifulSoup/#Download

The Beautiful Soup documentation is available at: http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html

To generate the HTML file in an Alice program, go to File -> Export Code for Printing

USAGE: python parser.py [FILEPATH to 1 HTML file]

OUTPUT: Prints the content of "methods" and "functions". These are two dicts that map a string (the method or function name) to the root node of that particular method. For each root node, this traverses the tree to print out its content. 

TREE STRUCTURE: 

Each method/function begins with a ROOT node and then a DoInOrder ndoe. The content of the method/function is placed in here. Different Alice constructs have their own Node subclass e.g If_Node, Else_Node.

FILE DESCRIPTIONS: 
- parser.py - contains the main method and parsing code
- util.py - defines the Stack and Nesting data structures

Node classes: 
- calls.py - Method_Call and Function_Call classes
- do_node.py - Do_Together and Do_In_Order classes
- doubles_operators_operations.py - Double_Node, Operator, Operation classes
- if_else.py - If_Node and Else_Node classes
- lists_for_each.py - For_Each_In_Order, For_Each_Together, List_Node classes
- node.py - parent Node class
- root_option1_sequence_first.py - Root_Node, Option1_Node, Sequence classes
- strings_and_functions.py - String_Node, Simple_Function1, Simple_Function2, Complex_Function, True_Node, False_Node classes
- vars_and_return.py - Return_Node class (and variable classes, but not implemented yet)
- wait_loop_while.py - Wait_Node, Loop_Node, While_Node classes


WHAT IS CURRENTLY SUPPORTED: 
- "basic methods" such as move, roll, turn
- If/else statements
- loops
- while loops
- Do in order
- Do Together (but does not handle concurrency issue yet)
- method calls
- mathematical operations
- distance to, is within, is at least (conditions)
- world methods (but not object specific methods, yet)
- functions - return types, function calls in conditions (but still working on this so it might be a little buggy at this point) 
