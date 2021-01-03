import datetime
import os
from mimetypes import MimeTypes
from pathlib import Path

from printfilesystem.model.json_model import JsonModel
from printfilesystem.utils.py_utils_ids import generate_name_id
from printfilesystem.utils.py_utils_ids import generate_namespace
from printfilesystem.utils.py_utils_string import default_if_empty
from printfilesystem.utils.py_utils_string import is_blank
from printfilesystem.utils.py_utils_string import substring_after_last

date_format = '%Y-%m-%d %H:%M:%S'


def write_json_to_file(json_path, json_model: JsonModel):
    file = open(json_path + os.sep + json_model.get_name() + '.json', 'w')
    file.write(json_model.__str__())
    pass


class CreateJson:
    def __init__(self, files_in_path, json_path):
        self.files_in_path = files_in_path
        self.json_path = json_path

    def create(self):
        mime = MimeTypes()
        for file in self.files_in_path:
            path = Path(file)
            json_file_name = path.name
            size = path.stat().st_size

            json_model = JsonModel(generate_name_id(os.sep, path, json_file_name, size))
            json_model.set_path(path.absolute().__str__())
            json_model.set_name(json_file_name)
            json_model.set_namespace(generate_namespace(json_model.get_path(), json_model.get_name(), "(.*)(anime/)(.*)"))
            json_model.set_size(size)

            created = datetime.datetime.fromtimestamp(path.stat().st_ctime).strftime(date_format)
            modified = datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime(date_format)
            json_model.set_created(created.__str__())
            json_model.set_modified(modified.__str__())

            mime__type = mime.guess_type(path)
            mime_str = mime__type[0]
            if is_blank(mime__type[0]):
                extension = substring_after_last(file, '.')
                mime_str = default_if_empty(extension, '')
            json_model.set_mime(mime_str)

            write_json_to_file(self.json_path, json_model)
        return None
