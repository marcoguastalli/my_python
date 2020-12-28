import os

from printfilesystem.py_utils import create_folder_if_not_exist
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.read_json import ReadJson


def main():
    source_path = "/home/marco27/Documents"
    target_path = "/home/marco27/temp/Documents"
    read_folder = ReadFolder(source_path, target_path)
    files_in_path = read_folder.read_folder()
    print("The folder with path '%s' contains %s files" % (source_path, files_in_path.__len__()))

    create_folder_if_not_exist(target_path)
    file = open(target_path + os.sep + 'output.txt', 'w')
    for line in files_in_path:
        file.write(line.__str__() + "\n")
    file.close()

    folder_path = "/home/marco27/Documents/json/"
    read_json = ReadJson(folder_path)
    files_in_path = read_json.read_path()
    print("The folder with path '%s' contains %s files" % (folder_path, files_in_path.__len__()))
    exit(0)


if __name__ == "__main__":
    main()
