import heapq


# Huffman tree
class Node:  
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
def get_frequency(filename):
    # read the text and determine the frequency of each character
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

def build_tree(frequency):
    # build the Huffman tree
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_code(node, code, codes):
    # prefix code table generation
    if node is not None:
        if node.char is not None:
            codes[node.char] = code
        generate_code(node.left, code + '0', codes)
        generate_code(node.right, code + '1', codes)

def fetch_codes(tree):
    codes = {}
    generate_code(tree, "", codes)
    return codes

def write_header(filename, frequency):
    with open(filename, 'wb') as f:
        for char, freq in frequency.items():
            f.write(char.encode('utf-8'))
            f.write(freq.to_bytes(4, byteorder='big'))

def encode_text(filename, text, codes):
    encoded_text = ''.join([codes[char] for char in text])
    byte_array = bytearray()
    # in steps of 8. The reason for this is that a byte consists of 8 bits.
    for i in range(0, len(encoded_text), 8):
        byte_array.append(int(encoded_text[i:i+8], 2))
    with open(filename, 'ab') as f:
        f.write(byte_array)

def decode_header(filename):
    # decode the header to get the frequency table
    frequency = {}
    with open(filename, 'rb') as f:
        while True:
            char = f.read(1)
            if not char:
                break
            freq = int.from_bytes(f.read(4), byteorder='big')
            frequency[char.decode('utf-8')] = freq
    return frequency

def decode_text(filename, tree):
    # decode the encoded text using the Huffman tree
    decoded_text = ""
    with open(filename, 'rb') as f:
        f.seek(len(frequency) * 5)  # Skip the header
        encoded_data = f.read()
        encoded_bits = ''.join(format(byte, '08b') for byte in encoded_data)
        
        current_node = tree
        for bit in encoded_bits:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
            
            if current_node.char is not None:
                decoded_text += current_node.char
                current_node = tree

    return decoded_text

if __name__ == "__main__":
    # This is a basic example of how to use the tool to compress a file
    input_file = "path_to_input.txt"
    output_file = "path_to_output.huffbitsqueeze"

    frequency = get_frequency(input_file)
    tree = build_tree(frequency)
    codes = fetch_codes(tree)

    write_header(output_file, frequency)
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    encode_text(output_file, text, codes)


    # Decoding
    # frequency = decode_header(output_file)
    # tree = build_tree(frequency)
    # decoded_text = decode_text(output_file, tree)

    # with open("decoded_output.txt", 'w', encoding='utf-8') as f:
    #     f.write(decoded_text)
