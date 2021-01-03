import unittest

import py_utils_string


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_convert_list_to_string(self):
            list_of_strings = ["one", "two", "three"]
            expected = 'onetwothree'
            self.assertEqual(expected, py_utils_string.convert_list_to_string(list_of_strings))

        def test_create_json_array_string_from_string_list(self):
            list_of_strings = ["one", "two", "three"]
            expected = '["one","two","three"]'
            result = py_utils_string.create_json_array_string_from_string_list(list_of_strings)
            self.assertEqual(expected, result)

        def test_substring_before_last(self):
            s = "/media/marco27/MyBook/wd8/anime/Avventura/One Piece/001 - Inizia l'avventura.mkv"
            separator = '/'
            expected = '/media/marco27/MyBook/wd8/anime/Avventura/One Piece'
            result = py_utils_string.substring_before_last(s, separator)
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(Test)
