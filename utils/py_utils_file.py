import os
from pathlib import Path


def create_folder_if_not_exists(path):
    if len(path) == 0:
        return
    if not os.path.exists(path):
        os.makedirs(path)


def delete_folder_if_exists(path):
    if len(path) == 0:
        return
    if os.path.exists(path):
        os.rmdir(path)


def recursive_read_folder(result, source_folder):
    files_in_folder = sorted(source_folder.iterdir())
    for file_in_folder in files_in_folder:
        element = file_in_folder
        if file_in_folder.is_dir():
            # element = "[" + element.__str__() + "]"
            recursive_read_folder(result, file_in_folder)
        result.append(element)


def write_strings_to_file(strings: list, target_path: str, target_file_name: str):
    if strings.__len__() == 0:
        return
    file = open(target_path + os.sep + target_file_name, 'w')
    for line in strings:
        file.write(line.__str__() + "\n")
    file.close()


def read_file_to_list_of_string(file_path: Path):
    file = open(file_path, 'r', encoding='UTF-8')
    file_content = file.readlines()
    file.close()
    return file_content
