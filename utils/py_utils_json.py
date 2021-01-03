import json
from utils.model.json_model import JsonModel


def read_json(json_as_string):
    json_object = json.loads(json_as_string)
    json_model = JsonModel(json_object['id'])
    json_model.set_path(json_object['path'])
    json_model.set_name(json_object['name'])
    json_model.set_namespace(json_object['namespace'])
    json_model.set_mime(json_object['mime'])
    json_model.set_created(json_object['created'])
    json_model.set_modified(json_object['modified'])
    json_model.set_size(json_object['size'])
    return json_model
