from node import Node

class Double_Node( Node ): 
    # v is a double
    def __init__(self, v): # extends Node.__init__
        self.value = v

    def print_children(self, indent_level): 
        print "Value = " + self.value

class Operator( Node ): 
    # o is a string
    def __init__(self, o): 
        self.type = "Operator"
        self.op = o

    def print_children(self, indent_level): 
        print op

class Operation( Node ): 
    # o is an Operator, d1 and d2 are Double_Nodes
    def __init__(self, o, d1, d2): 
        self.op = o
        self.set_left_child(d1)
        self.set_right_child(d2)

    def print_children(self, indent_level): 
        # TODO assert(left_child != NULL && op != NULL && right_child != NULL); 
        self.left_child.print_node(indent_level + 1, "(L)")
        self.op.print_node(indent_level + 1)
        self.right_child.print_node(indent_level + 1, "(R)")