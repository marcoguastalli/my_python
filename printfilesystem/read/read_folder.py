from pathlib import Path


class ReadFolder:
    def __init__(self, source_path, target_path):
        self.source_path = source_path
        self.target_path = target_path

    def read_folder(self):
        result = []
        source_folder = Path(self.source_path)
        files_in_folder = source_folder.iterdir()
        for file_in_folder in files_in_folder:
            element = file_in_folder
            if file_in_folder.is_dir():
                element = "[" + element.__str__() + "]"
            result.append(element)
        return result
