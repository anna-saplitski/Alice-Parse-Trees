from node import Node
"""
class If_Else( Node ): 
    def __init__(self): 
        Node.__init__(self)
        self.type = 'IfElseInOrder'

    def print_children(self, indent_level): 
        if self.left_child is not None: 
            self.left_child.print_node(indent_level+1, '(IF)')
        if self.right_child is not None: 
            self.right_child.print_node(indent_level+1, 'ELSE')
"""
class If_Node( Node ): 
    """
    left_node is the condition
    right_node is the sequence of actions 
    """
    def __init__(self): 
        Node.__init__(self)
        self.type = 'IF'

    def print_children(self, indent_level): 
        if self.left_child is not None: 
            self.left_child.print_node(indent_level + 1, "(CONDITION)")
        if self.right_child is not None: 
            self.right_child.print_node(indent_level + 1, "(ACTIONS)")


class Else_Node( Node ): 
    """
    contains the action / sequence of actions
    """
    def __init__(self): 
        Node.__init__(self)
        self.type = 'ELSE'
    def print_children(self, indent_level): 
        if self.left_child is not None: 
            self.left_child.print_node(indent_level + 1, "(ACTIONS)")
        if self.right_child is not None: 
            self.right_child.print_children(indent_level + 1)
