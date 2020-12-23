from pathlib import Path


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
            print(f'Content of %s:\n %s' % (file_name, file_content))
            file.close()
        return files_in_path
