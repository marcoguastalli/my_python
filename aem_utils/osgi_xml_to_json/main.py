from dotenv import dotenv_values
from pathlib import Path
from constants import DOT
from constants import XML_EXTENSION
from aem_utils.aem_constants import DIR_CONFIG_OSGICONFIG_CONFIG, OSGI_CONFIG_EXTENSION
from utils.py_utils_file import read_files_in_folder_filter_by_extension, read_file_to_list_of_string
from osgi_xml_to_json_converter import OsgiXmlToJsonConverter
from utils.py_utils_string import substring_before_last


def main():
    config = dotenv_values(".env")
    aem_source_code_base_path = config["aem_source_code_base_path"]

    path_to_osgiconfigs = Path(aem_source_code_base_path + DIR_CONFIG_OSGICONFIG_CONFIG)
    print(f"\nRead XML files from: {path_to_osgiconfigs}\n")

    converter = OsgiXmlToJsonConverter()

    xml_files_in_osgiconfig_folder = []
    read_files_in_folder_filter_by_extension(xml_files_in_osgiconfig_folder, path_to_osgiconfigs, XML_EXTENSION)
    for xml_file_name in xml_files_in_osgiconfig_folder:
        print(f"Converting file: {xml_file_name}")
        file_content = read_file_to_list_of_string(xml_file_name)
        print(f" - {file_content}")

        json_file_name = substring_before_last(xml_file_name, DOT) + DOT + OSGI_CONFIG_EXTENSION
        print(f"Writing new file: {json_file_name}")

    exit(0)


if __name__ == "__main__":
    main()
