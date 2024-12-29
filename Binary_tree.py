from Node import Node
class BinaryTree():
    
    def __init__(self,root) -> None:
        self.root = root
        self.inorder = ""
        self.preorder = ""
        self.encoded_dict = {}
        self.decoded_text = ""

    
    def postorder_traversals(self, node):
        
        postorder = ""

        if isinstance(node, Node):
            if node.left:
                postorder += self.postorder_traversals(node.left)
            if node.right:
                postorder += self.postorder_traversals(node.right)

            # Add the current node's symbol to the postorder string
            if str(node.symbol) == "\n":
                postorder += '\\n' + ","
            elif str(node.symbol) == "\'":
                postorder += "\\'" + ","
            elif str(node.symbol) == "\r":
                postorder += "\\r" + ","
            elif str(node.symbol) == "\"":
                postorder += '\\"' + ","
            elif str(node.symbol) == "\t":
                postorder += "\\t" + ","
            elif str(node.symbol) == "\b":
                postorder += "\\b" + ","
            elif str(node.symbol) == "\f":
                postorder += "\\f" + ","
            elif str(node.symbol) == "\a":
                postorder += '\\a' + ","
            elif str(node.symbol) == "\v":
                postorder += "\\v" + ","
            else:
                postorder += str(node.symbol) + ","

        return postorder



    def inorder_traversals(self, node):
        
        inorder = ""

        if isinstance(node, Node):
            if node.left:
                inorder += self.inorder_traversals(node.left)

            # Add the current node's symbol to the inorder string
            if str(node.symbol) == "\n":
                inorder += '\\n' + ","
            elif str(node.symbol) == "\'":
                inorder += "\\'" + ","
            elif str(node.symbol) == "\r":
                inorder += "\\r" + ","
            elif str(node.symbol) == "\"":
                inorder += '\\"' + ","
            elif str(node.symbol) == "\t":
                inorder += "\\t" + ","
            elif str(node.symbol) == "\b":
                inorder += "\\b" + ","
            elif str(node.symbol) == "\f":
                inorder += "\\f" + ","
            elif str(node.symbol) == "\a":
                inorder += '\\a' + ","
            elif str(node.symbol) == "\v":
                inorder += "\\v" + ","
            else:
                inorder += str(node.symbol) + ","

            if node.right:
                inorder += self.inorder_traversals(node.right)

        return inorder


    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        if isinstance(node, Node):
            print(" " * (4 * level) + prefix + str(node.symbol) + f" (Instance: {node.instance}, Code: {node.code})")
            if node.left:
                self.print_tree(node.left, level + 1, prefix="L--- ")
            if node.right:
                self.print_tree(node.right, level + 1, prefix="R--- ")

    def encode_nodes(self, root:Node=None, code=""):
        """
        Scan and update the tree, encoding each letter with binary code.
        Args:
            root (Node): Starting node for encoding. Defaults to the tree root.
            code (str): Binary code to assign to the current node. Defaults to "".
        """
        if root is None:
            root = self.root

        root.extend_encoding(code)

        if root.left is None and root.right is None:
            self.encoded_dict[root.symbol] = root.code
            return

        if root.right:
            self.encode_nodes(root.right, root.code + "1")
        if root.left:
            self.encode_nodes(root.left, root.code + "0")


    def decode_binary_string(self, binary_string):
        """
        Decodes a binary string using a dictionary that maps characters to binary sequences.

        Args:
            binary_string (str): The binary string to decode.


        Returns:
            str: The decoded text.
        """
        # Reverse the dictionary to map binary sequences to their corresponding characters
        reversed_dict = {value: key for key, value in self.encoded_dict.items()}
        
        decoded_text = ""
        current_sequence = ""
        
        for bit in binary_string:
            current_sequence += bit  # Build the current binary sequence
            
            if current_sequence in reversed_dict:  # Check if it matches any sequence in the dictionary
                char = reversed_dict[current_sequence]  # Append the corresponding character
                if str(char) == "\\n":
                    char = '\n' 
                elif str(char) == "\\'":
                    char = "\'" 
                elif str(char) == "\\r":
                    char = "\r" 
                elif str(char) == "\\t":
                    char = "\t" 
                elif str(char) == "\\b":
                    char = "\b" 
                elif str(char) == "\\f":
                    char = "\f" 
                elif str(char) == "\\a":
                    char = '\a' 
                elif str(char) == "\\v":
                    char += "\v" 
                decoded_text += char
                current_sequence = ""  # Reset the current sequence for the next match
        
        return decoded_text
   
      