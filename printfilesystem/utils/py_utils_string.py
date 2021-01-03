def convert_list_to_string(strings: list):
    return ''.join(strings)


def create_json_array_string_from_string_list(strings: list):
    result = '['
    count = 0
    for s in strings:
        count += 1
        result += '"' + s + '"'
        if count < strings.__len__():
            result += ','
    result += ']'
    return result
