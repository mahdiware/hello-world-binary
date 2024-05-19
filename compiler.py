import sys
import re

def hex_to_num(hex_char):
    """
    Convert a single hexadecimal character to its numerical value.
    """
    code = ord(hex_char)
    if 48 <= code <= 57:  # 0-9
        return code - 48
    elif 65 <= code <= 70:  # A-F
        return code - 55
    elif 97 <= code <= 102:  # a-f
        return code - 87
    else:
        raise ValueError("ERROR: No such hex value")

def process_file(input_file):
    """
    Read the input file, process its contents to convert strings to their 
    hexadecimal representation and numbers within parentheses to their 
    hexadecimal byte values. Finally, write the processed data to a binary file.
    """
    # Read the file content
    with open(input_file, 'r', encoding='utf8') as f:
        data = f.read()

    # Split file content into lines
    lines = data.split('\n')

    # Remove comments from each line
    code_lines = [line.split('//')[0] for line in lines]

    # Convert strings to hexadecimal representation
    strings_splitted = []
    for line in code_lines:
        parts = line.split('"')
        for i in range(1, len(parts), 2):
            parts[i] = ' ' + ' '.join(f"{ord(char):02x}" for char in parts[i]) + ' '
        strings_splitted.append(''.join(parts))

    # Convert numbers within parentheses to hexadecimal byte values
    numbers_splitted = []
    for line in strings_splitted:
        parts = re.split(r'([\(\)])', line)
        for i in range(1, len(parts), 2):
            num = int(parts[i])
            if num < -128 or num > 255:
                raise ValueError("ERROR: Number out of bounds.")
            if num < 0:
                num += 256
            parts[i] = f"{num:02x}"
        numbers_splitted.append(''.join(parts))

    # Join the processed lines and split by whitespace to get individual bytes
    bytes_str = ' '.join(numbers_splitted).split()

    # Convert hexadecimal byte values to integers
    bytes_list = []
    for byte in bytes_str:
        if len(byte) == 2:
            byte_value = 16 * hex_to_num(byte[0]) + hex_to_num(byte[1])
        elif len(byte) == 8:
            byte_value = sum(2**i * hex_to_num(byte[7-i]) for i in range(8))
        else:
            raise ValueError("ERROR: Cannot parse byte")
        bytes_list.append(byte_value)

    # Convert list of integers to bytes
    binary_data = bytes(bytes_list)

    # Write the bytes to a binary file
    with open('a.out', 'wb') as out_file:
        out_file.write(binary_data)

if __name__ == "__main__":
    # Ensure an input file is specified as a command-line argument
    if len(sys.argv) < 2:
        raise ValueError("ERROR: No input file specified")
    
    # Get the input file path from the command-line arguments
    input_file = sys.argv[1]
    
    # Process the input file
    process_file(input_file)

