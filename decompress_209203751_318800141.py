from Node import Node
import Binary_tree
import argparse
import os
import re







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
            "padding":lines[1][0].rstrip(),
            "inorder": lines[2].rstrip(),
            "postorder": lines[3].rstrip(),
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

        restore_tree = recreate_tree(data['inorder'],data['postorder'])
        restore_tree.print_tree()
        binary_text = decode_ascii_text(data["content"],data["padding"])
        print("Compressed")
        print (binary_text)
        print(restore_tree.encoded_dict)
        real_text = restore_tree.decode_binary_string(binary_text)
        print(real_text)


        

    except RuntimeError as e:
        print(e)



if __name__ == "__main__":
    main()
    

