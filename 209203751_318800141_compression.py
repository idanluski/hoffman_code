
import string
import os
import heapq

class Node:
    ID = 0
    def __init__(self, symbol=None, instance=1,left=None,right=None):
        self.symbol = symbol
        self.instance = instance
        self.id = Node.ID
        self.left = left
        self.right = right
        self.code = None
        Node.ID += 1

    def __lt__(self, other):
        return self.instance < other.instance

    # def __repr__(self):
    #     return f"Node(Node={self.Node}, instance={self.instance})"
    
    def __repr__(self):
        return f"{self.code}"
    
    def increment_instance(self):
        self.instance += 1

    def is_Node_is_symbol(self):
        res = True if self.symbol != None else False
        return res
    
    def extend_encoding(self,code):
        if self.code:
            self.code += code
        else:
            self.code = code

# Default path
default_path = 'harry_potter.txt'

# Check if a file path is provided via an environment variable or prompt
file_path = os.getenv('INPUT_FILE', default_path)

try:
    with open(file_path, 'r') as file:
        data = file.read()
except FileNotFoundError:
    print(f"File not found at {file_path}. Please check the path.")



# Initialize the dictionary with keys as non-digit characters and values as 0
symbol_dict = {}

#Count the instance of each Node
data = "abbcccddddeeeee"
for char in data:
    if char.isdigit():
        continue
    if char not in symbol_dict:
        symbol_dict[char] = Node(char)
    else:
        symbol_dict[char].increment_instance()
print(symbol_dict)

#Make Node heap
Node_heap = []
for node in symbol_dict.values():
    heapq.heappush(Node_heap,node)

def build_tree(Node_heap : list):
    for i in range(len(Node_heap)-1):
        smallest = heapq.heappop(Node_heap) #get smallest number and remove from heap
        second_smallest = heapq.heappop(Node_heap) #get second smallest number and remove from heap
        node = Node(instance=smallest.instance + second_smallest.instance,left=smallest,right=second_smallest)
        heapq.heappush(Node_heap,node)
    return Node_heap[0]

root = build_tree(Node_heap) #return the tree of su, of each node


def encode_nodes(root,code):
    """
    Scan  and update the tree, encode each letter in the bynary code
    """
    root.extend_encoding(code)
    if root.right == None and root.left == None:
        return
    if root.right != None:
        encode_nodes(root.right,root.code + "1")
    if root.left != None:
        encode_nodes(root.left,root.code + "0")    



encode_nodes(root,"")
print(symbol_dict) 
encoded_data_str =""
encodede_text = ""
for char in data:
    encoded_data_str += symbol_dict[char].code
i=0
for i in range(0,len(encoded_data_str),8):
    
    if len(encoded_data_str) < 8 :#edge
        char = encoded_data_str + "".join(["0" for i in range(8-  encoded_data_str)])
        decimal_value = int(char, 2)
        character = chr(decimal_value)
        break
    
    if i + 8 < len(encoded_data_str):#edge
        pass
    char = encoded_data_str[i:i + 8]
    decimal_value = int(char, 2)
    character = chr(decimal_value)    
    print(encoded_data_str)       