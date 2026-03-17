class Bookmarks:

    def __init__(self, title, uri, folder):
        self.__title = title
        self.__uri = uri
        self.__folder = folder
        self.__icon = ''
        self.__status = 200
        self.__created = ''
        self.__modified = ''

    def set_folder(self, folder):
        self.__folder = folder

    def set_icon(self, icon):
        self.__icon = icon

    def set_status(self, status):
        self.__status = status

    def set_created(self, created):
        self.__created = created

    def set_modified(self, modified):
        self.__modified = modified

    def get_title(self):
        return self.__title

    def get_uri(self):
        return self.__uri

    def get_folder(self):
        return self.__folder

    def get_icon(self):
        return self.__icon

    def get_status(self):
        return self.__status

    def get_created(self):
        return self.__created

    def get_modified(self):
        return self.__modified

    def __str__(self):
        result = '{' \
                 + '"title":"' + self.__title + '",' \
                 + '"uri":"' + self.__uri + '",' \
                 + '"folder":"' + self.__folder + '",' \
                 + '"icon":"' + self.__icon + '",' \
                 + '"status":' + self.__status.__str__() + ',' \
                 + '"created":"' + self.__created + '",' \
                 + '"modified":"' + self.__modified + '"' \
                 + "}"
        return result
