import json
from pathlib import Path
from json_bean import JsonBean


def convert_list_to_string(list_of_string):
    return ''.join(list_of_string)


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

            file_content_as_string = convert_list_to_string(file_content)
            json_as_string = self.read_json(file_content_as_string)

            # print('Content of %s:\n %s' % (file_name, json_as_string))

        return files_in_path

    @staticmethod
    def read_json(json_as_string):
        json_object = json.loads(json_as_string)
        jsonBean = JsonBean(json_object['uuid'])
        jsonBean.add_path(json_object['path'])
        jsonBean.set_name(json_object['name'])
        jsonBean.set_mime(json_object['mime'])
        jsonBean.set_created(json_object['created'])
        jsonBean.set_modified(json_object['modified'])
        jsonBean.set_size(json_object['size'])
        print(jsonBean)
        return jsonBean

