class JsonModel:

    def __init__(self, uuid):
        self.__uuid = uuid
        self.__path = list()
        self.__name = ''
        self.__mime = ''
        self.__created = ''
        self.__modified = ''
        self.__size = 0

    def add_path(self, path):
        self.__path.append(path)

    def set_paths(self, paths: list):
        self.__path = paths

    def set_name(self, name):
        self.__name = name

    def set_mime(self, mime):
        if mime is None:
            mime = ''
        self.__mime = mime

    def set_created(self, created):
        self.__created = created

    def set_modified(self, modified):
        self.__modified = modified

    def set_size(self, size):
        self.__size = size

    def get_name(self):
        return self.__name

    def get_paths(self):
        return self.__path

    # create a json-string with a counter and the paths of the list
    def get_paths_json_string(self):
        paths = self.get_paths()
        paths_as_string = '['
        count = 0
        for path in paths:
            count += 1
            paths_as_string += '"' + path + '"'
            if count < paths.__len__():
                paths_as_string += ','
        paths_as_string += ']'
        return paths_as_string

    def __str__(self):
        paths_as_string = self.get_paths_json_string()

        result = '{' \
                 + '"uuid":"' + self.__uuid + '",' \
                 + '"paths":' + paths_as_string + ',' \
                 + '"name":"' + self.__name + '",' \
                 + '"mime":"' + self.__mime + '",' \
                 + '"created":"' + self.__created + '",' \
                 + '"modified":"' + self.__modified + '",' \
                 + '"size":' + self.__size.__str__() \
                 + "}"
        return result
