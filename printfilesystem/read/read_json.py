import json
from pathlib import Path

import printfilesystem.utils.py_utils as py_utils
from printfilesystem.model.json_model import JsonModel


class ReadJson:
    def __init__(self, sourcePath):
        self.sourcePath = sourcePath

    def read_path(self):
        files_in_path = []
        folder_files = Path(self.sourcePath).rglob('*.json')
        for file_name in folder_files:
            files_in_path.append(file_name)

            file = open(file_name, 'r')
            file_content = file.readlines()
            file.close()

            file_content_as_string = py_utils.convert_list_to_string(file_content)

            json_bean = self.read_json(file_content_as_string)
            print('Content of %s:\n %s' % (file_name, json_bean))

        return files_in_path

    @staticmethod
    def read_json(json_as_string):
        json_object = json.loads(json_as_string)
        json_model = JsonModel(json_object['uuid'])
        json_model.set_paths(json_object['paths'])
        json_model.set_name(json_object['name'])
        json_model.set_mime(json_object['mime'])
        json_model.set_created(json_object['created'])
        json_model.set_modified(json_object['modified'])
        json_model.set_size(json_object['size'])
        return json_model
