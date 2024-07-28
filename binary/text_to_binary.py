def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary
