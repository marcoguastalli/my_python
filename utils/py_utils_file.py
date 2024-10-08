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


def recursive_read_folder(result, source_folder: Path):
    files_in_folder = sorted(source_folder.iterdir())
    for file_in_folder in files_in_folder:
        element = file_in_folder
        if file_in_folder.is_dir():
            # element = "[" + element.__str__() + "]"
            recursive_read_folder(result, file_in_folder)
        result.append(element)

def read_files_in_folder_filter_by_extension(result: [], source_folder: Path, extension: str):
    for subdir, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith(extension):
                result.append(subdir + os.sep + filename)
    return sorted(result)


def write_strings_to_file(strings: list, target_path: str, target_file_name: str):
    if strings.__len__() == 0:
        return
    with open(target_path + os.sep + target_file_name, 'w') as file:
        for line in strings:
            file.write(line.__str__() + "\n")
    pass

def write_strings_to_path_file_name(strings: list, target_path_file_name: str):
    if strings.__len__() == 0:
        return
    with open(target_path_file_name, 'w') as file:
        for line in strings:
            file.write(line.__str__())
    pass


def read_file_to_list_of_string(file_path: Path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        file_content = file.readlines()
        return file_content
    pass
