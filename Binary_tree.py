
from Node import Node
class BinaryTree():
    
    def __init__(self,root) -> None:
        self.root = root
        self.inorder = ""
        self.preorder = ""


    def preorder_traversals(self, node):
            if isinstance(node, Node):
                if str(node.symbol) == "\n":
                    self.preorder += '\\n' + ","
                elif str(node.symbol) == "\'":
                    self.preorder += "\\'" + ","
                elif str(node.symbol) == "\r":
                    self.preorder += "\\r" + ","
                elif str(node.symbol) == "\"":
                    self.preorder += '\\"' + ","
                elif str(node.symbol) == "\t":
                    self.preorder += "\\t" + ","
                elif str(node.symbol) == "\b":
                    self.preorder += "\\b" + ","
                elif str(node.symbol) == "\f":
                    self.preorder += "\\f" + ","
                elif str(node.symbol) == "\a":
                    self.preorder += '\\a' + ","
                elif str(node.symbol) == "\v":
                    self.preorder += "\\v" + ","
                else:
                    self.preorder += str(node.symbol) + ","
                if node.is_leaf():
                    return
                self.preorder_traversals(node.left)
                self.preorder_traversals(node.right)
            return

    def inorder_traversals(self, node):
        if isinstance(node, Node):
            if node.is_leaf():
                if str(node.symbol) == "\n":
                    self.inorder += '\\n' + ","
                elif str(node.symbol) == "\'":
                    self.inorder += "\\'" + ","
                elif str(node.symbol) == "\r":
                    self.inorder += "\\r" + ","
                elif str(node.symbol) == "\"":
                    self.inorder += '\\"' + ","
                elif str(node.symbol) == "\t":
                    self.inorder += "\\t" + ","
                elif str(node.symbol) == "\b":
                    self.inorder += "\\b" + ","
                elif str(node.symbol) == "\f":
                    self.inorder += "\\f" + ","
                elif str(node.symbol) == "\a":
                    self.inorder += '\\a' + ","
                elif str(node.symbol) == "\v":
                    self.inorder += "\\v" + ","
                else:
                    self.inorder += str(node.symbol) + ","
                return
            self.inorder_traversals(node.left)
            if str(node.symbol) == "\n":
                self.inorder += '\\n' + ","
            elif str(node.symbol) == "\'":
                self.inorder += "\\'" + ","
            elif str(node.symbol) == "\r":
                self.inorder += "\\r" + ","
            elif str(node.symbol) == "\"":
                self.inorder += '\\"' + ","
            elif str(node.symbol) == "\t":
                self.inorder += "\\t" + ","
            elif str(node.symbol) == "\b":
                self.inorder += "\\b" + ","
            elif str(node.symbol) == "\f":
                self.inorder += "\\f" + ","
            elif str(node.symbol) == "\a":
                self.inorder += '\\a' + ","
            elif str(node.symbol) == "\v":
                self.inorder += "\\v" + ","
            else:
                self.inorder += str(node.symbol) + ","
            self.inorder_traversals(node.right)
        return