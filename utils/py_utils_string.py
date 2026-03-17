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


def substring_before_first(s: str, separator: str):
    return s[:s.index(separator)]


def substring_after_last(s: str, separator: str):
    return s.rsplit(separator, 1)[1]


def substring_after_first(s: str, separator: str):
    return s.split(separator, 1)[1]


def is_blank(obj):
    if obj is None:
        return True
    elif is_empty(obj):
        return True
    return False


def is_empty(s: str):
    if s == "":
        return True
    return False


def default_if_empty(s: str, default_s: str):
    if is_blank(s):
        return default_s
    return s


def string_not_blank(s: str):
    return bool(s and s.strip())


def string_strip(s: str):
    if is_blank(s):
        return False
    return s.strip() if s != s.strip() else s
