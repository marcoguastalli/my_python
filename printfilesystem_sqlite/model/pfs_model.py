class PfsFile:

    def __init__(self, id):
        self.__id = id
        self.__path = ''
        self.__name = ''
        self.__namespace = ''
        self.__mime = ''
        self.__width = ''
        self.__height = ''
        self.__duration = ''
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

    def set_width(self, width):
        self.__width = width

    def set_height(self, height):
        self.__height = height

    def set_duration(self, duration):
        self.__duration = duration

    def set_created(self, created):
        self.__created = created

    def set_modified(self, modified):
        self.__modified = modified

    def set_size(self, size):
        self.__size = size

    def get_id(self):
        return self.__id

    def get_path(self):
        return self.__path

    def get_name(self):
        return self.__name

    def get_namespace(self):
        return self.__namespace

    def get_mime(self):
        return self.__mime

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_duration(self):
        return self.__duration

    def get_created(self):
        return self.__created

    def get_modified(self):
        return self.__modified

    def get_size(self):
        return self.__size

    def __str__(self):
        result = '{' \
                 + '"_id":"' + self.__id + '",' \
                 + '"path":"' + self.__path + '",' \
                 + '"name":"' + self.__name + '",' \
                 + '"namespace":"' + self.__namespace + '",' \
                 + '"mime":"' + self.__mime + '",' \
                 + '"width":"' + self.__width + '",' \
                 + '"height":"' + self.__height + '",' \
                 + '"duration":"' + self.__duration + '",' \
                 + '"created":"' + self.__created + '",' \
                 + '"modified":"' + self.__modified + '",' \
                 + '"size":' + self.__size.__str__() \
                 + "}"
        return result
