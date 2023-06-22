from constants import DOUBLE_QUOTE, EQUAL
from utils.py_utils_string import substring_before_first, substring_after_first, substring_before_last

MULTI_VALUE_PROPERTY_IDENTIFIER = "=\"["


class OsgiXmlToJsonConverter:

    def __init__(self):
        self.xml_lines = []

    def add_line(self, line: str):
        self.xml_lines.append(line)

    def get_json_object(self):
        result = {}
        for line in self.xml_lines:
            key = substring_before_first(line, EQUAL)
            if line.__contains__(MULTI_VALUE_PROPERTY_IDENTIFIER):
                value = []
            else:
                value = substring_after_first(line, DOUBLE_QUOTE)
                value = substring_before_last(value, DOUBLE_QUOTE)
            result[key] = value
        return result
