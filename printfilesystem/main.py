from read_json import ReadJson

def main():
    folder_path = "/home/marco27/Documents/json/"
    readJson = ReadJson(folder_path)
    files_in_path = readJson.read_path()
    print("The folder with path '%s' contains %s files" % (folder_path, files_in_path.__len__()))
    exit(0)


if __name__ == "__main__":
    main()
