import json
from pathlib import Path

from dotenv import dotenv_values

from aem_utils.aem_constants import OSGI_CONFIG_EXTENSION
from aem_utils.aem_constants import JCR
from constants import DOT, LESS, SLASH, UTF_8, XML_EXTENSION
from osgi_xml_to_json_converter import OsgiXmlToJsonConverter
from utils.py_utils_file import read_files_in_folder_filter_by_extension, read_file_to_list_of_string
from utils.py_utils_string import substring_before_last, string_not_blank


def main():
    config = dotenv_values(".env")
    aem_osgiconfig_absolute_path = config["aem_osgiconfig_absolute_path"]

    path_to_osgiconfigs = Path(aem_osgiconfig_absolute_path)
    print(f"\nRead XML files from: {path_to_osgiconfigs}\n")

    xml_files_in_osgiconfig_folder = []
    read_files_in_folder_filter_by_extension(xml_files_in_osgiconfig_folder, path_to_osgiconfigs, XML_EXTENSION)
    for xml_file_name in xml_files_in_osgiconfig_folder:
        print(f"Converting file: {xml_file_name}")

        # create new object to store the key/values
        converter = OsgiXmlToJsonConverter()

        # processing file content
        file_content = read_file_to_list_of_string(xml_file_name)
        for line in file_content:
            if string_not_blank(line) and not line.lstrip().rstrip().startswith((LESS, SLASH, JCR)):
                converter.add_line(line.lstrip().rstrip())

        # write json file
        json_file_name = substring_before_last(xml_file_name, DOT) + DOT + OSGI_CONFIG_EXTENSION
        print(f"Writing new file: {json_file_name}")
        with open(json_file_name, 'w', encoding=UTF_8) as f:
            json.dump(converter.get_json_object(), f, ensure_ascii=False, indent=4)

    exit(0)


if __name__ == "__main__":
    main()
