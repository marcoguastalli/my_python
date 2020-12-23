class JsonBean:

    def __init__(self, uuid):
        self.__uuid = uuid
        self.__path = list()
        self.__name = None
        self.__mime = None
        self.__created = None
        self.__modified = None
        self.__size = 0

    def add_path(self, path):
        self.__path.append(path)

    def set_name(self, name):
        self.__name = name

    def set_mime(self, mime):
        self.__mime = mime

    def set_created(self, created):
        self.__created = created

    def set_modified(self, modified):
        self.__modified = modified

    def set_size(self, size):
        self.__size = size

    def get_paths(self):
        return self.__path

    def __str__(self):
        # paths_as_string = '"path:"'
        paths_as_string = '{'
        count = 0
        for path in self.__path:
            count += 1
            paths_as_string += '"' + count.__str__() + '":"' + path + '"'
        paths_as_string += '}'

        result = '{' \
                 + '"uuid":"' + self.__uuid + '",' \
                 + '"paths":' + paths_as_string + ',' \
                 + '"name":"' + self.__name + '",' \
                 + '"mime":"' + self.__mime + '",' \
                 + '"created":"' + self.__created + '",' \
                 + '"modified":"' + self.__modified + '"' \
                 + "}"
        return result
