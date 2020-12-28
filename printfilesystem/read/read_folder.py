from pathlib import Path
import printfilesystem.py_utils as py_utils
import os


class ReadFolder:
    def __init__(self, source_path, target_path):
        self.source_path = source_path
        self.target_path = target_path

    def read_folder(self):
        source_folder = Path(self.source_path)
        result = ["[" + source_folder.__str__() + "]"]
        py_utils.recursive_read_folder(result, source_folder)
        return result

    def read_folder_using_os(self):
        result = []
        for subdir, dirs, files in os.walk(self.source_path):
            for filename in files:
                result.append(subdir + os.sep + filename)
        return sorted(result)
