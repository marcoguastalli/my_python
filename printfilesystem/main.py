from printfilesystem.create.create_json_from_path import CreateJsonFromPath
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.read.read_json import ReadJson
from printfilesystem.utils.py_utils import create_folder_if_not_exist


def main():
    source_path = "/home/marco27/Documents"
    json_path = "/home/marco27/temp/json"
    create_folder_if_not_exist(json_path)

    read_folder = ReadFolder(source_path)
    files_in_path = read_folder.read_folder_using_os()
    print("The folder with path '%s' contains %s paths" % (source_path, files_in_path.__len__()))

    create_json = CreateJsonFromPath(files_in_path, json_path)
    create_json.create()

    read_json = ReadJson(json_path)
    files_in_path = read_json.read_path()
    print("The folder with path '%s' contains %s json files" % (json_path, files_in_path.__len__()))
    exit(0)


if __name__ == "__main__":
    main()
