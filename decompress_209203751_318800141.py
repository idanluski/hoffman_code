from Node import Node
import Binary_tree
import argparse
import os
import re


SAFE_ASCII = ''.join(chr(i) for i in range(33, 127))  # '!' to '~'
SAFE_ASCII_SIZE = len(SAFE_ASCII)  # 94 characters

# Map values to safe ASCII characters
VALUE_TO_SAFE = {i: SAFE_ASCII[i % SAFE_ASCII_SIZE] for i in range(256)}
SAFE_TO_VALUE = {v: k for k, v in VALUE_TO_SAFE.items()}

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




def decode_value_with_escape(encoded_char, reverse_mapping):
    """
    Decode a character or escape sequence back to its decimal value.
    
    Args:
        encoded_char (str): Encoded character or escape sequence.
        reverse_mapping (dict): Reverse mapping of escape sequences to decimal values.
    
    Returns:
        int: Decoded decimal ASCII value.
    """
    if encoded_char.startswith("\\e"):
        return reverse_mapping[encoded_char]
    return ord(encoded_char)
    

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

def retrieve_file_content(file_path):
    """
    Reads and splits the content of the file at the given path into lines.
    
    Args:
        file_path (str): The path to the file.
    
    Returns:
        dict: A dictionary containing `content`, `postorder`, and `inorder` data.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            print(lines[1][0])
        
        if len(lines) < 3:
            raise ValueError("File does not contain the expected 3 lines.")
        
        return {
            "content": lines[0].strip(),
            "padding":lines[1][0].strip(),
            "postorder": lines[2].strip(),
            "inorder": lines[3].strip()
        }
    except Exception as e:
        raise RuntimeError(f"Error reading file '{file_path}': {e}")

# def decode_to_binary(encoded_text,reverse_mapping):
#     decoded_binary = ""
#     i = 0
#     while i < len(encoded_text):
#         if encoded_text[i:i+2] == "\\e":  # Check for escape sequence
#             # Find the full escape sequence
#             escape_seq = encoded_text[i:encoded_text.index("\\", i + 2) + 2]
#             decimal_value = decode_value_with_escape(escape_seq, reverse_mapping)
#             decoded_binary += format(decimal_value, '08b')
#             i += len(escape_seq)  # Skip escape sequence
#         else:
#             decimal_value = decode_value_with_escape(encoded_text[i], reverse_mapping)
#             decoded_binary += format(decimal_value, '08b')
#             i += 1
#     return decoded_binary

def decode_text(encoded_text, reverse_mapping):
    """
    Decode text with escape sequences back to binary.
    
    Args:
        encoded_text (str): Encoded string with escape sequences.
        reverse_mapping (dict): Reverse mapping of escape sequences to decimal values.
    
    Returns:
        str: Decoded binary string.
    """
    decoded_binary = ""
    i = 0
    while i < len(encoded_text):
        if encoded_text[i:i+2] == "\\e":  # Check for escape sequence
            # Match the escape sequence pattern
            match = re.match(r"\\e\d+", encoded_text[i:])
            if match:
                escape_seq = match.group(0)
                decimal_value = decode_value_with_escape(escape_seq, reverse_mapping)
                decoded_binary += format(decimal_value, '08b')
                i += len(escape_seq)  # Move the pointer past the escape sequence
            else:
                raise ValueError(f"Invalid escape sequence at position {i}")
        else:
            decimal_value = decode_value_with_escape(encoded_text[i], reverse_mapping)
            decoded_binary += format(decimal_value, '08b')
            i += 1
    return decoded_binary

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Retrieve and split content from a file.")
    
    # Add an argument for the file path
    parser.add_argument(
        "path",
        type=str,
        help="The path to the file to retrieve content from"
    )
    
    # Parse the arguments
    #args = parser.parse_args()
    
    # Get the path from the arguments
   # input_path = args.path
    
    # Validate the path
    # if not os.path.exists(input_path):
    #     print(f"Error: The path '{input_path}' does not exist.")
    #     return
    
    # if not os.path.isfile(input_path):
    #     print(f"Error: The path '{input_path}' is not a file.")
    #     return
    
    # Retrieve and process the content of the file
    try:
        input_path =r"/Users/iluski/Desktop/Hoffman_code/compressed_data.txt" #TODO remove this in the end!!!
        data = retrieve_file_content(input_path)
        print(f"Content of the file '{input_path}':")
        print(f"1. Content: {data['content']}")
        print(f"2. padding: {data['padding']}")
        print(f"3. Postorder: {data['postorder']}")
        print(f"4. Inorder: {data['inorder']}")

        restore_tree = recreate_tree(data['postorder'],data['inorder'])
        restore_tree.print_tree()
        map, reverse_map = create_mapping()
        binary_text = decode_text(data["content"],reverse_map)
        real_text = restore_tree.decompression(binary_text)


        

    except RuntimeError as e:
        print(e)



if __name__ == "__main__":
    main()
    

