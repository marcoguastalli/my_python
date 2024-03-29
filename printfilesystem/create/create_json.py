import datetime
import os
from mimetypes import MimeTypes
from pathlib import Path

from metadata_hachoir.src.metadata_hachoir import extract_metadata
from printfilesystem.model.pfs_model import PfsFile
from rabbitmq.publish_message import publish_message
from utils.py_utils_ids import generate_name_id
from utils.py_utils_ids import generate_namespace
from utils.py_utils_string import default_if_empty
from utils.py_utils_string import is_blank
from utils.py_utils_string import substring_after_last
from utils.py_utils_string import substring_before_last

date_format = '%Y-%m-%d %H:%M:%S'


class CreateJson:
    def __init__(self, rabbitmq_host, rabbitmq_login, rabbitmq_secret, rabbitmq_queue, files_in_path):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_login = rabbitmq_login
        self.rabbitmq_secret = rabbitmq_secret
        self.rabbitmq_queue = rabbitmq_queue
        self.files_in_path = files_in_path

    def create_and_publish(self):
        mime = MimeTypes()
        for file in self.files_in_path:
            posix_path = Path(file)
            file_name = posix_path.name
            size = posix_path.stat().st_size
            psf_id = generate_name_id(os.sep, posix_path, file_name, size)
            path_no_file_name = substring_before_last(posix_path.absolute().__str__(), os.sep)

            pfs_model = PfsFile(psf_id)
            pfs_model.set_path(path_no_file_name)
            pfs_model.set_name(file_name)
            namespace = generate_namespace(pfs_model.get_path(), pfs_model.get_name(), "(.*)(anime/)(.*)")
            pfs_model.set_namespace(default_if_empty(namespace, ''))
            pfs_model.set_size(size)

            created = datetime.datetime.fromtimestamp(posix_path.stat().st_ctime).strftime(date_format)
            modified = datetime.datetime.fromtimestamp(posix_path.stat().st_mtime).strftime(date_format)
            pfs_model.set_created(created.__str__())
            pfs_model.set_modified(modified.__str__())

            if '.' in file:
                extension = substring_after_last(file, '.')
                if extension == 'BUP':
                    pfs_model.set_mime('BUP')
                elif extension == 'IFO':
                    pfs_model.set_mime('IFO')
                elif extension == 'DS_Store':
                    pfs_model.set_mime('DS_Store')
                else:
                    print("Extract metadata from: %s" % file)
                    metadata: dict = extract_metadata(file)
                    if metadata is not None and metadata.get('result') == 'ok':
                        mime_str = metadata['mime_type'][0]
                        if metadata.__contains__('width'):
                            pfs_model.set_width(metadata['width'][0])
                        else:
                            pfs_model.set_width('')
                        if metadata.__contains__('height'):
                            pfs_model.set_height(metadata['height'][0])
                        else:
                            pfs_model.set_height('')
                        if metadata.__contains__('duration'):
                            pfs_model.set_duration(metadata['duration'][0])
                        else:
                            pfs_model.set_duration('')
                    else:
                        mime__type = mime.guess_type(posix_path.__str__())
                        mime_str = mime__type[0]
                        if is_blank(mime__type[0]):
                            extension = substring_after_last(file, '.')
                            mime_str = default_if_empty(extension, '')
                    pfs_model.set_mime(mime_str)
            else:
                pfs_model.set_mime('')

            json_unicode_string = u'' + pfs_model.__str__()
            self.publish_string_to_rabbit_queue(json_unicode_string)
        pass

    def publish_string_to_rabbit_queue(self, json_unicode_string: str):
        publish_message(self.rabbitmq_host, self.rabbitmq_login, self.rabbitmq_secret, self.rabbitmq_queue, json_unicode_string)
        pass
