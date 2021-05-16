import json
import os

from utils.model.json_model import JsonModel


def read_json(json_string):
    json_object = json.loads(json_string)
    json_model = JsonModel(json_object['id'])
    json_model.set_path(json_object['path'])
    json_model.set_name(json_object['name'])
    json_model.set_namespace(json_object['namespace'])
    json_model.set_mime(json_object['mime'])
    json_model.set_created(json_object['created'])
    json_model.set_modified(json_object['modified'])
    json_model.set_size(json_object['size'])
    return json_model


def write_json_to_file(json_path, json_file_name, json_string):
    try:
        json_unicode_string = u'' + json_string
        with open(json_path + os.sep + json_file_name, 'w') as file:
            file.write(json_unicode_string)
        pass
    except Exception as e:
        print("Error write json to file with json_string: %s" % json_string)
        print(e)
        return None
