class JsonModel:

    def __init__(self, id):
        self.__id = id
        self.__path = ''
        self.__name = ''
        self.__mime = ''
        self.__created = ''
        self.__modified = ''
        self.__size = 0

    def set_path(self, path):
        self.__path = path

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

    def __str__(self):
        result = '{' \
                 + '"id":"' + self.__id + '",' \
                 + '"name":"' + self.__name + '",' \
                 + '"path":"' + self.__path + '",' \
                 + '"mime":"' + self.__mime + '",' \
                 + '"created":"' + self.__created + '",' \
                 + '"modified":"' + self.__modified + '",' \
                 + '"size":' + self.__size.__str__() \
                 + "}"
        return result
