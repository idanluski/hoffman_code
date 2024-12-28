class Node:
    ID = 0
    def __init__(self, symbol=None, instance=1,left=None,right=None):
        
        self.instance = instance #Number instances of Symbol 
        self.id = Node.ID
        self.left = left
        self.right = right
        self.code = None
        self.symbol = str(symbol) if symbol else str(self.id)#Symbol e.g 'A', '$' ...
        Node.ID += 1

    def __lt__(self, other):
        return self.instance < other.instance

    # def __repr__(self):
    #     return f"Node(Node={self.Node}, instance={self.instance})"
    
    def __repr__(self):
        return f"{self.code}"
    
    def increment_instance(self):
        """Increment instance by 1 """
        self.instance += 1

    def is_Node_is_symbol(self):
        """Check if Node contain a symbol char, thos nodes are the leaf"""
        res = True if self.symbol != None else False
        return res
    def is_leaf(self):
        if self.symbol.isdigit():
            return False
        
        return True
    def extend_encoding(self,code):
        """add 0 or 1 to encoding according to tree"""
        if self.code:
            self.code += code
        else:
            self.code = code
