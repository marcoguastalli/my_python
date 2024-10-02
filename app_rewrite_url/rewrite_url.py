import os

from app_rewrite_url.rewrite_url_constants import REWRITE_RULE
from app_rewrite_url.rewrite_url_constants import REWRITE_RULE_FLAGS
from app_rewrite_url.rewrite_url_constants import INPUT_FILE_NAME_WITH_PATTERNS
from app_rewrite_url.rewrite_url_constants import INPUT_FILE_NAME_WITH_SUBSTITUTIONS
from app_rewrite_url.rewrite_url_constants import OUTPUT_FILE_NAME_WITH_REWRITE_RULES
from utils.py_utils_string import is_blank
from pathlib import Path
from utils.py_utils_file import write_strings_to_path_file_name
from utils.py_utils_file import read_file_to_list_of_string

def main():
    patterns = []
    substitutions = []
    file_path_patterns = Path(os.environ['MY_HOME'] + INPUT_FILE_NAME_WITH_PATTERNS)
    file_path_substitutions = Path(os.environ['MY_HOME'] + INPUT_FILE_NAME_WITH_SUBSTITUTIONS)
    file_content_patterns = read_file_to_list_of_string(file_path_patterns)
    file_content_substitutions = read_file_to_list_of_string(file_path_substitutions)
    for line in file_content_patterns:
        if not is_blank(line) and line != "\n":
            patterns.append(line)
    for line in file_content_substitutions:
        if not is_blank(line) and line != "\n":
            substitutions.append(line)

    write_strings_to_path_file_name(substitutions, os.environ['MY_HOME'] + OUTPUT_FILE_NAME_WITH_REWRITE_RULES)
    pass


if __name__ == "__main__":
    main()
