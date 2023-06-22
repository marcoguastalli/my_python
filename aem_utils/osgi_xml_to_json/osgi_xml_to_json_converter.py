from utils.py_utils_file import read_file_to_list_of_string
import json

class OsgiXmlToJsonConverter:

    def createJsonObject(self):
        data = {}
        data['key'] = 'value'
        return json.dumps(data)
