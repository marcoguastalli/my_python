import shutil

from printfilesystem.create.create_json import CreateJson
from printfilesystem.read.read_folder import ReadFolder
from printfilesystem.read.read_json import ReadJson
from printfilesystem.store.store__json import StoreJson
from utils.py_utils_file import create_folder_if_not_exists


def main():
    source_path = "/media/marco27/Data/DiscoD/video/anime/toTransfer"
    target_path = "/home/marco27/temp/json"
    create_folder_if_not_exists(target_path)

    rf = ReadFolder(source_path)
    files_in_folder = rf.read_files_in_folder_using_os()
    print("The folder with path '%s' contains %s files" % (source_path, files_in_folder.__len__()))

    cj = CreateJson(files_in_folder, target_path)
    cj.create()
    print("Created json in folder '%s'" % target_path)

    rj = ReadJson(target_path)
    json_string_list = rj.create_json_string_list_from_path()
    print("The folder with path '%s' contains %s json files" % (target_path, json_string_list.__len__()))

    # remove target_path folder
    shutil.rmtree(target_path, ignore_errors=False, onerror=None)

    stored_json_list = []
    for json_sting in json_string_list:
        sj = StoreJson(json_sting)
        stored_json = sj.store('http://localhost:8980/marco27-web/v1/pfs/create')
        stored_json_list.append(stored_json)
        # print("Stored json '%s'" % stored_json)
    print("Stored %s json from folder '%s'" % (stored_json_list.__len__(), source_path))

    exit(0)


if __name__ == "__main__":
    main()
