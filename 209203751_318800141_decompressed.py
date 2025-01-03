from Node import Node
import Binary_tree
import argparse
import os
import re
import base64



filename = "209203751_318800141_decompressed.txt"

def write_to_file(filename: str, data: str):
    """
    Write a string to a new file.

    Args:
        filename (str): Name of the file to write to.
        data (str): The string data to write into the file.
    """
    try:
        # Open the file in write mode (creates a new file if it doesn't exist)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
        print(f"Data successfully written to {filename}.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


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
        with open(file_path, "r",encoding='utf-8') as file:
            lines = file.readlines()
            print(lines[1][0])
        
        if len(lines) < 3:
            raise ValueError("File does not contain the expected 3 lines.")
        
        return {
            "content": lines[0].rstrip(),
            "padding":lines[1].rstrip(),
            "inorder": lines[2].rstrip(),
            "postorder": lines[3].rstrip(),
        }
    except Exception as e:
        raise RuntimeError(f"Error reading file '{file_path}': {e}")

def decode_base64(encoded_str: str) -> bytes:
    return base64.b64decode(encoded_str)

def unpack_bytes_to_bits(data: bytes, real_bit_length: str) -> str:
    """
    Convert a bytes object back to a bitstring of length real_bit_length.
    We assume the original bitstring length is known (stored) as real_bit_length.
    """
    real_bit_length = int(real_bit_length)
    bitstring = ""
    for b in data:
        # Format each byte as 8 bits: e.g. 197 -> '11000101'
        bitstring += f"{b:08b}"

    # Slice off any padding bits
    return bitstring[:real_bit_length]

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
    args = parser.parse_args()
    
    # Get the path from the arguments
    input_path = args.path
    
    # Validate the path
    if not os.path.exists(input_path):
        print(f"Error: The path '{input_path}' does not exist.")
        return
    
    if not os.path.isfile(input_path):
        print(f"Error: The path '{input_path}' is not a file.")
        return
    
    #Retrieve and process the content of the file
    try:
        data = retrieve_file_content(input_path)
        print(f"Content of the file '{input_path}':")
        print(f"1. Content: {data['content']}")
        print(f"2. padding: {data['padding']}")
        print(f"3. Postorder: {data['postorder']}")
        print(f"4. Inorder: {data['inorder']}")

        restore_tree = recreate_tree(data['inorder'],data['postorder'])
        restore_tree.print_tree()


        decoded_b64 = decode_base64(data["content"])
        unpacked_bits = unpack_bytes_to_bits(decoded_b64, data["padding"])
        print("Unpacked bits:", unpacked_bits)
        real_text = restore_tree.decode_binary_string(unpacked_bits)
        write_to_file(filename=filename,data=real_text)

 


        

    except RuntimeError as e:
        print(e)



if __name__ == "__main__":
    main()
    

