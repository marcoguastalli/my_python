def binary_number_to_text(binary_number):
    binary_str = format(binary_number, 'b')
    # Make sure the binary string length is a multiple of 8
    padded_binary_str = binary_str.zfill((len(binary_str) + 7) // 8 * 8)
    text = ''.join(chr(int(padded_binary_str[i:i + 8], 2)) for i in range(0, len(padded_binary_str), 8))
    return text
