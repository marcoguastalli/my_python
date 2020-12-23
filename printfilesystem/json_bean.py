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

    def set_created(self, mime):
        self.__mime = mime

    def set_modified(self, modified):
        self.__modified = modified

    def set_size(self, size):
        self.__size = size

    def __str__(self):
        return "{name: '" + self.__name + "'}"
