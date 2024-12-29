import string
import os
import heapq
from Node import Node
import Binary_tree
import re

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



   
def encode_ascii_value(ascii_value):
    """
    Encodes a single ASCII value into a printable character or a mapped sequence.

    Args:
        ascii_value (int): The ASCII value to encode.

    Returns:
        str: Encoded representation of the ASCII value.
    """
    if ascii_value == 92:  # ASCII for '\'
        return "\\x5C"  # Explicitly encode backslash as '\x5C'
    elif 32 <= ascii_value <= 126:  # Printable range
        return chr(ascii_value)
    else:
        return f"\\x{ascii_value:02X}"  # Encode non-printable ASCII as '\xNN'

def decode_ascii_text(encoded_text, padding_bits=0):
    """
    Decodes an encoded string into a binary representation, removing padding bits.

    Args:
        encoded_text (str): The encoded text to decode.
        padding_bits (int): The number of padding bits to remove from the end.

    Returns:
        str: Decoded binary string with padding removed.
    """
    decoded_binary = []
    i = 0

    while i < len(encoded_text):
        if encoded_text[i:i+2] == "\\x":  # Encoded non-printable ASCII
            ascii_value = int(encoded_text[i+2:i+4], 16)  # Convert hex to int
            decoded_binary.append(f"{ascii_value:08b}")  # Convert to binary
            i += 4
        else:  # Printable character
            ascii_value = ord(encoded_text[i])
            decoded_binary.append(f"{ascii_value:08b}")  # Convert to binary
            i += 1

    # Join all binary values into a single binary string
    binary_string = ''.join(decoded_binary)

    # Remove padding bits from the end
    padding_bits_str = int(padding_bits)
    if padding_bits_str > 0:
        binary_string = binary_string[:-padding_bits_str]

    return binary_string

print(len(encoded_data_str))
buffering = len(encoded_data_str)%8
for i in range(0,len(encoded_data_str),8):
   
    if (len(encoded_data_str)<8) or ((i+8) >= len(encoded_data_str)) :#edge
        char = encoded_data_str[i:]
        buffering= 8 - len(char)
        char += "0"*(buffering)
        decimal_value = int(char, 2)
        character = encode_ascii_value(decimal_value)
        encodede_text += character
        print(character)

        break
   
    if (i + 8) < len(encoded_data_str):#edge
        #pass
        char = encoded_data_str[i:i + 8]
        decimal_value = int(char, 2)
        character = encode_ascii_value(decimal_value)  
        #decode_char = decode_ascii_value(character)
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
ls = encodede_text.split("\n")
binary_text = decode_ascii_text(ls[0],buffering)
print(binary_text)
print(byiary_tree.encoded_dict)
real_text = assembled_tree.decode_binary_string(binary_text)
print(real_text)

# print("---------------------------")
# assembled_tree.print_tree()








