from read.read_folder import ReadFolder
from read_json import ReadJson


def main():
    source_path = "/home/marco27/Documents"
    target_path = "/home/marco27/temp/Documents"
    read_folder = ReadFolder(source_path, target_path)
    files_in_path = read_folder.read_folder()
    print("The folder with path '%s' contains %s files" % (source_path, files_in_path.__len__()))
    for file_in_path in files_in_path:
        print(file_in_path)

    # folder_path = "/home/marco27/Documents/json/"
    # read_json = ReadJson(folder_path)
    # files_in_path = read_json.read_path()
    # print("The folder with path '%s' contains %s files" % (folder_path, files_in_path.__len__()))
    exit(0)


if __name__ == "__main__":
    main()
