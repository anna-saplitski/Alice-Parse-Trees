from node import Node

"""
Double_Node (node that represents a double value)
    -> self.value -- if the value is hardcoded e.g 1.0, then self.value contains the value. 
    Otherwise, it is None. 
    -> self.left_child -- if the value is returned from a function call, then self.left_child
    contains the Function_Call
"""

class Double_Node( Node ): 
    # v is a double
    def __init__(self, v): 
        Node.__init__(self)
        # tries to parse v as a float. If it doesn't work, then it's a function. 
        try:
            self.value = float(v)
        except ValueError: 
            self.value = None
            self.left_child = Function_Call(v, None)
        self.type = 'Double'

    """
    Prints the child nodes accordingly. 
    """
    def print_children(self, indent_level): 
        if self.value is not None: 
            print "Value = " + str(self.value)
        else: 
            if self.left_child is not None: 
                self.left_child.print_node(indent_level + 1)

"""
Operator (node that represents an operator i.e +, -, *, / )
    -> self.left_child -- the operator value itself. (string)
"""
class Operator( Node ): 
    # o is a string
    def __init__(self, o): 
        Node.__init__(self)
        self.type = "Operator"
        self.left_child = o

    def print_children(self, indent_level): 
        print self.left_child,

"""
Operation (node that represents an operation e.g 2 + 4)
    self.left_child -- the left hand side of the operation. 
    self.op - the Operator node
    self.right_child -- the right side of the operation. Can either be a Double_Node or another
    Operation for nested operations e.g 2+2 - 4
"""

class Operation( Node ): 
    # o is an Operator, d1 and d2 are Double_Nodes
    def __init__(self, o): 
        Node.__init__(self)
        self.op = o
        self.type = 'Operation'

    def print_children(self, indent_level): 
        if self.left_child is not None:  
            self.left_child.print_node(indent_level + 1, "(L)")
        self.op.print_node(indent_level + 1)
        if self.right_child is not None: 
            self.right_child.print_node(indent_level + 1, "(R)")