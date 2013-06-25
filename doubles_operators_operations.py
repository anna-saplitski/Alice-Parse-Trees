from node import Node

class Double_Node( Node ): 
    # v is a double
    def __init__(self, v): 
        Node.__init__(self)
        try:
            self.value = float(v)
        except ValueError: 
            self.value = None
            self.left_child = Function_Call(v, None)
        self.type = 'Double'

    def print_children(self, indent_level): 
        if self.value is not None: 
            print "Value = " + str(self.value)
        else: 
            if self.left_child is not None: 
                self.left_child.print_node(indent_level + 1)

class Operator( Node ): 
    # o is a string
    def __init__(self, o): 
        Node.__init__(self)
        self.type = "Operator"
        self.op = o

    def print_children(self, indent_level): 
        print self.op,

class Operation( Node ): 
    # o is an Operator, d1 and d2 are Double_Nodes
    def __init__(self, o): 
        Node.__init__(self)
        self.op = o
        self.type = 'Operation'

    def print_children(self, indent_level): 
        # TODO assert(left_child != NULL && op != NULL && right_child != NULL);
        if self.left_child is not None:  
            self.left_child.print_node(indent_level + 1, "(L)")
        self.op.print_node(indent_level + 1)
        if self.right_child is not None: 
            self.right_child.print_node(indent_level + 1, "(R)")