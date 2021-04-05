import unittest

from duplicate_image_file import duplicate_image_file


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_get_tags_from_soup(self):
            source_file_name = "/Users/marcoguastalli/temp/vr46.jpg"
            target_file_name = "/Users/marcoguastalli/temp/vr46 (copy).jpg"
            result = duplicate_image_file(source_file_name, target_file_name)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(Test)
