import json
from pathlib import Path

import utils.py_utils_string as py_utils_string
from printfilesystem.model.json_model import JsonModel


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

            json_model = self.read_json(file_content_as_string)
            result.append(json_model)
            # print('Content of %s:\n %s' % (file_name, json_as_string))

        return result

    @staticmethod
    def read_json(json_as_string):
        json_object = json.loads(json_as_string)
        json_model = JsonModel(json_object['id'])
        json_model.set_path(json_object['path'])
        json_model.set_path(json_object['path'])
        json_model.set_name(json_object['namespace'])
        json_model.set_mime(json_object['mime'])
        json_model.set_created(json_object['created'])
        json_model.set_modified(json_object['modified'])
        json_model.set_size(json_object['size'])
        return json_model
