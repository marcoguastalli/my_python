from pathlib import Path

import utils.py_utils_string as py_utils_string
from utils.py_utils_file import read_file_to_list_of_string


class ReadJson:
    def __init__(self, source_path):
        self.sourcePath = source_path

    def create_json_string_list_from_path(self):
        result = []
        folder_files = Path(self.sourcePath).rglob('*.json')
        for file_name in folder_files:
            file_content = read_file_to_list_of_string(file_name)
            file_content_as_string = py_utils_string.convert_list_to_string(file_content)
            result.append(file_content_as_string)
        return result
