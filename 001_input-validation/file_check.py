"""
Document validation against predefined format
"""
import argparse
import csv
import errno
from pathlib import Path

from format_validator import FormatValidator


class FileCheck(object):

    def __init__(self):
        self.file = None
        # Parsing arguments of the invocation
        self.parser = argparse.ArgumentParser(description='Check csv file against predefined format')
        self.parser.add_argument('--file',
                                 help='file location')
        self._args = self.parser.parse_args()
        self.file = self._args.file

    def check_file(self) -> bool:
        if self.file is None:
            exit(errno.EINVAL)
        path = Path(str(self.file))
        if not path.exists():
            exit(errno.ENOENT)
        elif path.is_dir():
            exit(errno.EISDIR)

        # File correct
        fv = FormatValidator()
        with open(str(self.file), newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=";", quotechar="|")
            for row in reader:
                if not fv.check_valid_name(row[0]) or not fv.check_valid_surname(row[1]) \
                        or not fv.check_valid_phone(row[2]) or not fv.check_valid_email(row[3]):
                    return False
        return True


if __name__ == "__main__":
    fc = FileCheck()
    if fc.check_file():
        print("File format is valid")
        exit(0)
    else:
        print("File format not compliant")
        exit(1)
