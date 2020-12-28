import os


def convert_list_to_string(list_of_string):
    return ''.join(list_of_string)


def recursive_read_folder(result, source_folder):
    files_in_folder = sorted(source_folder.iterdir())
    for file_in_folder in files_in_folder:
        element = file_in_folder
        if file_in_folder.is_dir():
            # element = "[" + element.__str__() + "]"
            recursive_read_folder(result, file_in_folder)
        result.append(element)


def create_folder_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_strings_to_file(strings, target_path, target_file_name):
    file = open(target_path + os.sep + target_file_name, 'w')
    for line in strings:
        file.write(line.__str__() + "\n")
    file.close()
