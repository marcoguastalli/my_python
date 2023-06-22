from constants import EQUAL
from utils.py_utils_string import substring_before_first


class OsgiXmlToJsonConverter:

    def __init__(self):
        self.xml_lines = []

    def add_line(self, line: str):
        self.xml_lines.append(line)

    def get_json_object(self):
        result = {}
        for line in self.xml_lines:
            key = substring_before_first(line, EQUAL)
            value = "value"
            result[key] = value
        return result
