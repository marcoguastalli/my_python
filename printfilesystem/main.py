from printfilesystem.create.create_json import CreateJson
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.read.read_json import ReadJson
from printfilesystem.store.store__json import StoreJson
from printfilesystem.utils.py_utils import create_folder_if_not_exist


def main():
    source_path = "/home/marco27/Downloads"
    target_path = "/home/marco27/temp/json"
    create_folder_if_not_exist(target_path)

    rf = ReadFolder(source_path)
    files_in_folder = rf.read_files_in_folder_using_os()
    print("The folder with path '%s' contains %s paths" % (source_path, files_in_folder.__len__()))

    create_json = CreateJson(files_in_folder, target_path)
    create_json.create()
    print("Created json in folder '%s'", target_path)

    rj = ReadJson(target_path)
    json_in_folder = rj.get_json()
    print("The folder with path '%s' contains %s json files" % (target_path, json_in_folder.__len__()))

    for json_as_string in json_in_folder:
        sj = StoreJson(json_as_string)
        stored_json = sj.store()
        print("Stored json '%s'" % stored_json)
    print("Stored json from folder '%s'" % target_path)

    exit(0)


if __name__ == "__main__":
    main()
