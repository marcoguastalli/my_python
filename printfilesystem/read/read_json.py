from pathlib import Path

import utils.py_utils_string as py_utils_string


class ReadJson:
    def __init__(self, sourcePath):
        self.sourcePath = sourcePath

    def get_json_model(self):
        result = []
        folder_files = Path(self.sourcePath).rglob('*.json')
        for file_name in folder_files:
            file = open(file_name, 'r')
            file_content = file.readlines()
            file.close()

            file_content_as_string = py_utils_string.convert_list_to_string(file_content)
            result.append(file_content_as_string)
        return result
