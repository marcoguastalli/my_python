import unittest
from pathlib import Path

import py_utils_file


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_create_folder_if_not_exists(self):
            path = ''
            self.assertIsNotNone(self, py_utils_file.create_folder_if_not_exists(path))

        def test_delete_folder_if_exists(self):
            path = ''
            self.assertIsNotNone(self, py_utils_file.delete_folder_if_exists(path))

        def test_recursive_read_folder(self):
            source_folder = Path('')
            result = py_utils_file.recursive_read_folder([], source_folder)
            self.assertNotEqual(self, '', result)

        def test_write_strings_to_file(self):
            self.assertIsNotNone(self, py_utils_file.write_strings_to_file([], '', ''))


if __name__ == "__main__":
    unittest.main(Test)
