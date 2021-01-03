import uuid
import re


def generate_uuid():
    return uuid.uuid4().hex


def generate_name_id(separator, path, name, size):
    s = re.sub('[^0-9a-zA-Z]+', ' ', str(path) + separator + name + str(size)).strip()
    result = ''
    result += s[0].upper()
    for i in range(1, len(s)):
        if s[i] == ' ':
            result += s[i + 1].upper()
            i += 1
        elif s[i - 1] != ' ':
            result += s[i]
    return result
