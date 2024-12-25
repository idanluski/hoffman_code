
import string
import os
import heapq
import Node
import Binary_tree

# Default path
default_path = 'harry_potter.txt'

# Check if a file path is provided via an environment variable or prompt
file_path = os.getenv('INPUT_FILE', default_path)

try:
    with open(file_path, 'r') as file:
        data = file.read()
except FileNotFoundError:
    print(f"File not found at {file_path}. Please check the path.")


def prolematic_symbol(symbol):
    if str(symbol) == "\n":
        return '\\n' 
    elif str(symbol) == "\'":
        return "\\'" 
    return symbol

# Initialize the dictionary with keys as non-digit characters and values as 0
symbol_dict = {}

#Count the instance of each Node
data = "abbcccddddeeeee" #override the data to check quickly the code

#make a dictionary of nodes e.g {"a":<node contain 'a', ...}
for char in data:
    if char.isdigit():
        continue
    if char not in symbol_dict:
        char = prolematic_symbol(char)
        symbol_dict[char] = Node.Node(char)
    else:
        symbol_dict[char].increment_instance()
print(symbol_dict)

#Make Node heap as shown in the lecture
Node_heap = []
for node in symbol_dict.values():
    heapq.heappush(Node_heap,node)

def build_tree(Node_heap : list):
    for i in range(len(Node_heap)-1):
        smallest = heapq.heappop(Node_heap) #get smallest number and remove from heap
        second_smallest = heapq.heappop(Node_heap) #get second smallest number and remove from heap
        node = Node.Node(instance=smallest.instance + second_smallest.instance,left=smallest,right=second_smallest)
        heapq.heappush(Node_heap,node)
    return Node_heap[0]

root = build_tree(Node_heap) #return the tree of su, of each node
byiary_tree= Binary_tree.BinaryTree(root)
byiary_tree.inorder_traversals(root)
byiary_tree.preorder_traversals(root)
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

#[{symbol,code,},]

encode_nodes(root,"")
print(symbol_dict) 
encoded_data_str ="" #Encoded data, a sequence of 0 and 1 
encodede_text = ""
for char in data:
    char = prolematic_symbol(char)
    encoded_data_str += symbol_dict[char].code
#encoded_data_str += "11111111"
i=0
print(encoded_data_str)
size_encoded_data = len(encoded_data_str)


# Define a subset of safe ASCII characters (you can customize this range)
SAFE_ASCII = ''.join(chr(i) for i in range(33, 127))  # Excludes control characters
SAFE_ASCII_SIZE = len(SAFE_ASCII)

# Map values to safe ASCII characters
VALUE_TO_SAFE = {i: SAFE_ASCII[i % SAFE_ASCII_SIZE] for i in range(256)}
SAFE_TO_VALUE = {v: k for k, v in VALUE_TO_SAFE.items()}
   
def encode_value_with_escape(value, escape_char="\\"):
    if value < 0 or value > 255:
        raise ValueError("Value must be in the range 0ß–255.")
    if value>=0 and value <127:
        return chr(value)
    encoded_char = VALUE_TO_SAFE[value]
    # Escape the character if it already exists in the text
    if encoded_char in (escape_char, *SAFE_ASCII):
        return f"{escape_char}{encoded_char}"
    return encoded_char

for i in range(0,len(encoded_data_str),8):
   
    if (len(encoded_data_str)<8) or ((i+8) > len(encoded_data_str)) :#edge
        char = encoded_data_str[i:]
        buffering= 8 - len(char)
        char += "0"*(8- len(char))
        decimal_value = int(char, 2)
        
        encodede_text += character
        print(character)

        break
   
    if (i + 8) < len(encoded_data_str):#edge
        #pass
        char = encoded_data_str[i:i + 8]
        decimal_value = int(char, 2)
        character = encode_value_with_escape(decimal_value)  
        encodede_text += character


print(encodede_text) 
    


