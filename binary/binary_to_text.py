def binary_to_text(binary):
    text = ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))
    return text
