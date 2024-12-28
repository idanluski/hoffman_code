import string
import os
import heapq
from Node import Node
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
        symbol_dict[char] = Node(char)
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
        node = Node(instance=smallest.instance + second_smallest.instance,left=smallest,right=second_smallest)
        heapq.heappush(Node_heap,node)

    return Node_heap[0]

def write_to_compressed_file(data):
    """
    Write the given string to a file named 'compressed_data'.

    :param data: The string to write to the file
    """
    try:
        # Define the file name
        file_name = "compressed_data.txt"

        # Open the file in write mode and write the string
        with open(file_name, "w") as file:
            file.write(data)

        print(f"Data successfully written to '{file_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


root = build_tree(Node_heap) #return the tree of su, of each node
byiary_tree= Binary_tree.BinaryTree(root)
inorder = byiary_tree.inorder_traversals(root)
print(inorder)
 
postorder = byiary_tree.postorder_traversals(root)
print(postorder)

   

#[{symbol,code,},]
byiary_tree.encode_nodes()
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

def create_mapping():
    """
    Create a mapping for characters with ASCII values outside the printable range (33-126).
    Returns a dictionary for encoding and its reverse for decoding.
    """
    mapping = {}
    escape_prefix = "\\e"  # Escape prefix
    counter = 1  # Counter for unique escape sequences

    # Map all ASCII values outside the printable range
    for ascii_value in range(256):  # Full byte range
        if ascii_value < 33 or ascii_value > 126:
            mapping[ascii_value] = f"{escape_prefix}{counter}"
            counter += 1

    reverse_mapping = {v: k for k, v in mapping.items()}
    return mapping, reverse_mapping

map, reverse_map = create_mapping()

SAFE_ASCII = ''.join(chr(i) for i in range(33, 127))  # Safe characters: '!' to '~'
SAFE_ASCII_SIZE = len(SAFE_ASCII)  # 94 safe characters

VALUE_TO_SAFE = {i: SAFE_ASCII[i] if i < SAFE_ASCII_SIZE else SAFE_ASCII[i % SAFE_ASCII_SIZE] + str(i // SAFE_ASCII_SIZE) for i in range(256)}
SAFE_TO_VALUE = {v: k for k, v in VALUE_TO_SAFE.items()}

   
def encode_value_with_escape(decimal_value, mapping):
    """
    Encode a decimal value into a character or escape sequence.
    
    Args:
        decimal_value (int): Decimal ASCII value to encode.
        mapping (dict): Mapping of problematic characters to escape sequences.
    
    Returns:
        str: Encoded character or escape sequence.
    """
    if decimal_value in mapping:
        return mapping[decimal_value]
    return chr(decimal_value)

def decode_value_with_escape(encoded_char, reverse_mapping):
    """
    Decode a character or escape sequence back to its decimal value.
    
    Args:
        encoded_char (str): Encoded character or escape sequence.
        reverse_mapping (dict): Reverse mapping of escape sequences to decimal values.
    
    Returns:
        int: Decoded decimal ASCII value.
    """
    if encoded_char in reverse_mapping:
        return reverse_mapping[encoded_char]
    return ord(encoded_char)
print(len(encoded_data_str))

buffering=0
for i in range(0,len(encoded_data_str),8):
   
    if (len(encoded_data_str)<8) or ((i+8) > len(encoded_data_str)) :#edge
        char = encoded_data_str[i:]
        buffering= 8 - len(char)
        char += "0"*(buffering)
        decimal_value = int(char, 2)
        character = encode_value_with_escape(decimal_value,map)
        encodede_text += character
        print(character)

        break
   
    if (i + 8) < len(encoded_data_str):#edge
        #pass
        char = encoded_data_str[i:i + 8]
        decimal_value = int(char, 2)
        character = encode_value_with_escape(decimal_value,map)  
        decode_char = decode_value_with_escape(character,reverse_map)
        encodede_text += character

encodede_text += "\n"+str(buffering)+"\n"+inorder+"\n"+postorder

print(encodede_text) 

write_to_compressed_file(encodede_text)



def recreate_tree(inorder, postorder):
    """
    Recreates a binary tree using inorder and postorder traversal data.
    
    Args:
        inorder (str): Inorder traversal string, e.g., "c,6,a,5,b,8,d,7,e,"
        postorder (str): Postorder traversal string, e.g., "c,a,b,5,6,d,e,7,8,"
    
    Returns:
        BinaryTree: A binary tree constructed from the given traversals.
    """
    
    def parse_traversal(traversal):
        return traversal.rstrip(",").split(",")

    inorder_list = parse_traversal(inorder)
    postorder_list = parse_traversal(postorder)

    def build_tree(in_left, in_right):
        nonlocal postorder_list

        if in_left > in_right:
            return None

        # Pop the root symbol from the end of the postorder list
        root_symbol = postorder_list.pop()
        root = Node(symbol=root_symbol)

        # Find the index of the root in inorder list
        inorder_index = inorder_list.index(root_symbol)

        # Build the right subtree first, followed by the left subtree
        root.right = build_tree(inorder_index + 1, in_right)
        root.left = build_tree(in_left, inorder_index - 1)

        return root

    # Construct the tree
    root = build_tree(0, len(inorder_list) - 1)
    restore_tree = Binary_tree.BinaryTree(root)
    restore_tree.encode_nodes()
    
    # Create a BinaryTree instance and return it
    return restore_tree

assembled_tree = recreate_tree(inorder, postorder)
byiary_tree.print_tree()
print("---------------------------")
assembled_tree.print_tree()








