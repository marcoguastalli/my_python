import unittest

from utils.read_json_files_from_path import ReadJsonFilesFromPath


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_read_json_files_from_path(self):
            source_path = "/Users/marcoguastalli/dev/repository/git/my_python/999_test_resources"
            object_instance = ReadJsonFilesFromPath(source_path)
            result = object_instance.create_json_string_list_from_path()
            print(result)
            self.assertIsNotNone(self, result)
            self.assertTrue(self, type(result) is list)


if __name__ == "__main__":
    unittest.main(Test)
