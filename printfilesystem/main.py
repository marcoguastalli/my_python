import shutil

from printfilesystem.create.create_json import CreateJson
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.read.read_json import ReadJson
from printfilesystem.store.store__json import StoreJson
from printfilesystem.utils.py_utils_file import create_folder_if_not_exists


def main():
    source_path = "/media/marco27/Data/DiscoD"
    target_path = "/home/marco27/temp/json"
    create_folder_if_not_exists(target_path)

    rf = ReadFolder(source_path)
    files_in_folder = rf.read_files_in_folder_using_os()
    print("The folder with path '%s' contains %s files" % (source_path, files_in_folder.__len__()))

    create_json = CreateJson(files_in_folder, target_path)
    create_json.create()
    print("Created json in folder '%s'", target_path)

    rj = ReadJson(target_path)
    json_model_in_folder = rj.get_json_model()
    print("The folder with path '%s' contains %s json files" % (target_path, json_model_in_folder.__len__()))

    # remove directory
    shutil.rmtree(target_path, ignore_errors=False, onerror=None)

    for json_model in json_model_in_folder:
        sj = StoreJson(json_model)
        stored_json = sj.store()
        # print("Stored json '%s'" % stored_json)
    print("Stored json from folder '%s'" % source_path)

    exit(0)


if __name__ == "__main__":
    main()
