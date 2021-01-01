from printfilesystem.create.create_json import CreateJson
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.read.read_json import ReadJson
from printfilesystem.utils.py_utils import create_folder_if_not_exist


def main():
    source_path = "/home/marco27/Downloads"
    target_path = "/home/marco27/temp/json"
    create_folder_if_not_exist(target_path)

    read_folder = ReadFolder(source_path)
    files_in_folder = read_folder.read_files_in_folder_using_os()
    print("The folder with path '%s' contains %s paths" % (source_path, files_in_folder.__len__()))

    create_json = CreateJson(files_in_folder, target_path)
    create_json.create()
    print("Created json in folder '%s'", target_path)

    read_json = ReadJson(target_path)
    files_in_folder = read_json.read_path()
    print("The folder with path '%s' contains %s json files" % (target_path, files_in_folder.__len__()))
    exit(0)


if __name__ == "__main__":
    main()
