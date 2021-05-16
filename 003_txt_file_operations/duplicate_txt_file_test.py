import unittest

from duplicate_txt_file import duplicate_txt_file


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_get_tags_from_soup(self):
            source_file_name = "/Users/marcoguastalli/temp/source.txt"
            target_file_name = "/Users/marcoguastalli/temp/target.txt"
            result = duplicate_txt_file(source_file_name, target_file_name)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(Test)
