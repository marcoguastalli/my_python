class JsonModel:

    def __init__(self, id):
        self.__id = id
        self.__path = ''
        self.__name = ''
        self.__namespace = ''
        self.__mime = ''
        self.__created = ''
        self.__modified = ''
        self.__size = 0

    def set_path(self, path):
        self.__path = path

    def set_name(self, name):
        self.__name = name

    def set_namespace(self, namespace):
        self.__namespace = namespace

    def set_mime(self, mime):
        self.__mime = mime

    def set_created(self, created):
        self.__created = created

    def set_modified(self, modified):
        self.__modified = modified

    def set_size(self, size):
        self.__size = size

    def get_name(self):
        return self.__name

    def __str__(self):
        result = '{' \
                 + '"id":"' + self.__id + '",' \
                 + '"path":"' + self.__path + '",' \
                 + '"name":"' + self.__name + '",' \
                 + '"namespace":"' + self.__namespace + '",' \
                 + '"mime":"' + self.__mime + '",' \
                 + '"created":"' + self.__created + '",' \
                 + '"modified":"' + self.__modified + '",' \
                 + '"size":' + self.__size.__str__() \
                 + "}"
        return result
