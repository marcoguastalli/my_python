import json
from pathlib import Path

import py_utils
from json_bean import JsonBean


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
        json_bean = JsonBean(json_object['uuid'])
        json_bean.add_path(json_object['path'])
        json_bean.set_name(json_object['name'])
        json_bean.set_mime(json_object['mime'])
        json_bean.set_created(json_object['created'])
        json_bean.set_modified(json_object['modified'])
        json_bean.set_size(json_object['size'])
        return json_bean
