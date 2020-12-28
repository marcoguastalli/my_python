import os
import uuid
from mimetypes import MimeTypes
from pathlib import Path
import datetime


from printfilesystem.model.json_model import JsonModel


def write_json_to_file(json_path, json_model: JsonModel):
    file = open(json_path + os.sep + json_model.get_name() + '.json', 'w')
    file.write(json_model.__str__())
    pass


class CreateJsonFromPath:
    def __init__(self, files_in_path, json_path):
        self.files_in_path = files_in_path
        self.json_path = json_path

    def create(self):
        mime = MimeTypes()
        for file in self.files_in_path:
            path = Path(file)
            json_file_name = path.name
            json_model = JsonModel(uuid.uuid4().hex)
            json_model.set_name(json_file_name)
            json_model.add_path(path.absolute().__str__())
            json_model.set_size(path.stat().st_size)

            created = datetime.datetime.fromtimestamp(path.stat().st_ctime)
            modified = datetime.datetime.fromtimestamp(path.stat().st_mtime)
            json_model.set_created(created.__str__())
            json_model.set_modified(modified.__str__())

            mime__type = mime.guess_type(path)
            mime_str = mime__type[0]
            json_model.set_mime(mime_str)

            write_json_to_file(self.json_path, json_model)
        return None
