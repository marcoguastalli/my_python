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


def substring_before_last(s: str, separator: str):
    return s.rsplit(separator, 1)[0]


def is_empty(s: str):
    if s == "":
        return True
    return False


def default_if_empty(s: str, default_s: str):
    if is_empty(s):
        return default_s
    return s
