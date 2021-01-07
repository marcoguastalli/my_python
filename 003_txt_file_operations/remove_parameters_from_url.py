import os
from pathlib import Path

from utils.py_utils_file import read_file_to_list_of_string
from utils.py_utils_file import write_strings_to_file
from utils.py_utils_string import is_blank
from utils.py_utils_string import substring_after_last
from utils.py_utils_string import substring_before_last


def remove_parameters_from_url_in_file(source_file_name: str, target_file_name: str):
    result = []
    file_path = Path(source_file_name)
    file_content = read_file_to_list_of_string(file_path)
    for line in file_content:
        if not is_blank(line) and line != "\n":
            result.append(substring_before_last(line, '?'))

    write_strings_to_file(result, substring_before_last(target_file_name, os.sep),
                          substring_after_last(target_file_name, os.sep))
    return result
