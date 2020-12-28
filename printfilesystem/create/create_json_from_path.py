from pathlib import Path


class CreateJsonFromPath:
    def __init__(self, files_in_path, json_path):
        self.files_in_path = files_in_path
        self.json_path = json_path

    def create(self):
        for file in self.files_in_path:
            path = Path(file)
            print(path)
        return None
