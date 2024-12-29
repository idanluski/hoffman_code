import string
import os
import heapq
from Node import Node
import Binary_tree
import re
import base64

# Default path
default_path = 'sample_text.txt'

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
#data = "abbcccddddeeeee" #override the data to check quickly the code

#make a dictionary of nodes e.g {"a":<node contain 'a', ...}
for char in data:
    if char.isdigit():
        continue
    if char not in symbol_dict:
        #char = prolematic_symbol(char)
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
    #char = prolematic_symbol(char)
    encoded_data_str += symbol_dict[char].code
#encoded_data_str += "11111111"
i=0
print(encoded_data_str)
size_encoded_data = len(encoded_data_str)


def pack_bits_into_bytes(bitstring: str) -> bytes:
    """
    Convert a string of '0'/'1' characters into a bytes object.
    Pads the bitstring if it's not a multiple of 8 in length.
    """
    # Pad with zeros so length is multiple of 8
    padding_needed = (8 - (len(bitstring) % 8)) % 8
    bitstring_padded = bitstring + ('0' * padding_needed)

    # Each chunk of 8 bits -> one byte
    byte_array = bytearray()
    for i in range(0, len(bitstring_padded), 8):
        chunk = bitstring_padded[i:i+8]
        byte_val = int(chunk, 2)  # interpret as base-2
        byte_array.append(byte_val)

    return bytes(byte_array)
   
def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')  # get a str back

encoded_data_str_length = len(encoded_data_str)
packed = pack_bits_into_bytes(encoded_data_str)
print(len(encoded_data_str))
encoded_b64 = encode_base64(packed)
print("Base64 encoded:", encoded_b64)
buffering = len(encoded_data_str)%8

encoded_text_with_64 =encoded_b64 + "\n"+str(encoded_data_str_length)+"\n"+inorder+"\n"+postorder


write_to_compressed_file(encoded_text_with_64)



def recreate_tree(inorder, postorder):
    """
    Recreates a binary tree using inorder and postorder traversal data.
    
    Args:
        inorder (str): Inorder traversal string, e.g., "c,6,a,5,b,8,d,7,e,"
        postorder (str): Postorder traversal string, e.g., "c,a,b,5,6,d,e,7,8,"
    
    Returns:
        BinaryTree: A binary tree constructed from the given traversals.
    """
    
    def parse_traversal(s: str):
        """
        Splits `s` such that:
        - Single comma => skip
        - Multiple commas => ','
        - Single *or multiple* spaces => ' '
        - Everything else (letters, digits, backslashes, etc.) => keep as-is
        """
        # 1) Find all tokens that are either:
        #    - runs of non-comma-space chars: [^, ]+
        #    - runs of commas: ,+
        #    - runs of spaces:  +
        parts = re.findall(r'[^, ]+|,+| +', s)
        
        result = []
        for part in parts:
            # Is this `part` purely commas?
            if all(ch == ',' for ch in part):
                if len(part) == 1:
                    # single comma => delimiter => skip
                    continue
                else:
                    # multiple commas => add a single comma token
                    result.append(',')
            
            # Is this `part` purely spaces?
            elif all(ch == ' ' for ch in part):
                # whether 1 space or multiple, we always add a single " "
                result.append(' ')
            
            else:
                # Everything else (letters, digits, backslashes, etc.)
                result.append(part)
        
        return result
    inorder_list = parse_traversal(inorder)
    print(len(inorder_list))
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

#     # Construct the tree
    root = build_tree(0, len(inorder_list) - 1)
    restore_tree = Binary_tree.BinaryTree(root)
    restore_tree.encode_nodes()
    
    # Create a BinaryTree instance and return it
    return restore_tree

assembled_tree = recreate_tree(inorder, postorder)
byiary_tree.print_tree()
#----------------------------------------------decompress check
# ls = encodede_text.split("\n")
# binary_text = decode_ascii_text(ls[0],buffering)
# print(binary_text)
# print(byiary_tree.encoded_dict)
# real_text = assembled_tree.decode_binary_string(binary_text)
# print(real_text)

# print("---------------------------")
# assembled_tree.print_tree()








