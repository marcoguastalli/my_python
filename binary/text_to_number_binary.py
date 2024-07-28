def text_to_binary_number(text):
    binary_str = ''.join(format(ord(char), '08b') for char in text)
    binary_number = int(binary_str, 2)
    return binary_number
