import re
import uuid

from printfilesystem.utils.py_utils_string import substring_before_last


def generate_uuid():
    return uuid.uuid4().hex


def generate_name_id(separator, path, file_name, size):
    s = re.sub('[^0-9a-zA-Z]+', ' ', str(path) + separator + file_name + str(size)).strip()
    result = ''
    result += s[0].upper()
    for i in range(1, len(s)):
        if s[i] == ' ':
            result += s[i + 1].upper()
            i += 1
        elif s[i - 1] != ' ':
            result += s[i]
    return result


def generate_namespace(path, file_name, regexp):
    path_file_name = path + file_name
    g = re.match(regexp, path_file_name)
    if g.groups().__len__() == 3:
        return substring_before_last(g.group(3), file_name)
    else:
        return None
