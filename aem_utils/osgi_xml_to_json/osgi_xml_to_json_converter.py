from utils.py_utils_file import read_file_to_list_of_string
class OsgiXmlToJsonConverter:
    def __init__(self):
        print("init")

    def read_xml_file_content(self, file_name):

        file_content_as_string = read_file_to_list_of_string(file_name)
        for file_line in file_content_as_string:
            print(file_line)
