import json


class OsgiXmlToJsonConverter:

    def __init__(self):
        self.xml_lines = []

    def add_line(self, line: str):
        self.xml_lines.append(line)

    def get_json_object(self):
        data = {}
        data['key'] = 'value'
        return json.dumps(data)
