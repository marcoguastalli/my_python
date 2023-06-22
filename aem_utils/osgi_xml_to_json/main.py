
from dotenv import dotenv_values
from pathlib import Path
from constants import XML_EXTENSION
from aem_utils.aem_constants import DIR_CONFIG_OSGICONFIG_CONFIG
from utils.py_utils_file import read_files_in_folder_filter_by_extension

def main():
    config = dotenv_values(".env")
    aem_source_code_base_path = config["aem_source_code_base_path"]

    path_to_osgiconfigs = Path(aem_source_code_base_path + DIR_CONFIG_OSGICONFIG_CONFIG)
    print(f"\nRead XML files from: {path_to_osgiconfigs}\n")

    xml_files_in_osgiconfig_folder = []
    read_files_in_folder_filter_by_extension(xml_files_in_osgiconfig_folder, path_to_osgiconfigs, XML_EXTENSION)
    for file_in_folder in xml_files_in_osgiconfig_folder:
        print(f"{file_in_folder}")

    exit(0)


if __name__ == "__main__":
    main()