import os
import re


def convert_list_to_string(strings: list):
    return ''.join(strings)


def recursive_read_folder(result, source_folder):
    files_in_folder = sorted(source_folder.iterdir())
    for file_in_folder in files_in_folder:
        element = file_in_folder
        if file_in_folder.is_dir():
            # element = "[" + element.__str__() + "]"
            recursive_read_folder(result, file_in_folder)
        result.append(element)


def create_folder_if_not_exist(path):
    if len(path) == 0:
        return
    if not os.path.exists(path):
        os.makedirs(path)


def write_strings_to_file(strings: list, target_path, target_file_name):
    file = open(target_path + os.sep + target_file_name, 'w')
    for line in strings:
        file.write(line.__str__() + "\n")
    file.close()


def generate_name_id(separator, path, name, size):
    s = re.sub('[^0-9a-zA-Z]+', ' ', path + separator + name + str(size)).strip()
    result = ''
    result += s[0].upper()
    for i in range(1, len(s)):
        if s[i] == ' ':
            result += s[i + 1].upper()
            i += 1
        elif s[i - 1] != ' ':
            result += s[i]
    return result


def generate_namespace(path, name, pattern):
    path_file_name = path + name
    g = re.match(pattern, path_file_name)
    if g.groups().__len__() == 3:
        return g.group(3)
    else:
        return None
