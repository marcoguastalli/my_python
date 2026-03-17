import os
from pathlib import Path

import utils.py_utils_file as py_utils_file


class ReadFolder:
    def __init__(self, source_path):
        self.source_path = source_path

    def read_files_in_folder_using_os(self):
        result = []
        for subdir, dirs, files in os.walk(self.source_path):
            for filename in files:
                result.append(subdir + os.sep + filename)
        return sorted(result)
