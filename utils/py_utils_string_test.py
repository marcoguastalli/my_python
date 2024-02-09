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

        def test_substring_before_first(self):
            s = "/media/marco27/MyBook/wd8/anime/Avventura/One Piece/001 - Inizia l'avventura.mkv"
            separator = '-'
            expected = '/media/marco27/MyBook/wd8/anime/Avventura/One Piece/001 '
            result = py_utils_string.substring_before_first(s, separator)
            self.assertEqual(expected, result)

        def test_substring_after_last(self):
            s = "/media/marco27/MyBook/wd8/anime/Avventura/One Piece/001 - Inizia l'avventura.mkv"
            separator = '.'
            expected = 'mkv'
            result = py_utils_string.substring_after_last(s, separator)
            self.assertEqual(expected, result)

        def test_substring_after_first(self):
            s = "/media/marco27/MyBook/wd8/anime/Avventura/One Piece/001 - Inizia l'avventura.mkv"
            separator = ' - '
            expected = "Inizia l'avventura.mkv"
            result = py_utils_string.substring_after_first(s, separator)
            self.assertEqual(expected, result)

        def test_is_blank(self):
            self.assertTrue(py_utils_string.is_blank(None))
            self.assertTrue(py_utils_string.is_blank(''))
            self.assertFalse(py_utils_string.is_blank(True))
            self.assertFalse(py_utils_string.is_blank(False))

        def test_is_empty(self):
            self.assertTrue(py_utils_string.is_empty(''))
            self.assertTrue(py_utils_string.is_empty(""))
            self.assertFalse(py_utils_string.is_empty('s'))
            self.assertFalse(py_utils_string.is_empty("s"))

        def test_default_if_empty(self):
            self.assertEqual('s', py_utils_string.default_if_empty('s', 'd'))
            self.assertEqual('d', py_utils_string.default_if_empty('', 'd'))

        def test_string_not_blank(self):
            self.assertFalse(py_utils_string.string_not_blank(''))
            self.assertFalse(py_utils_string.string_not_blank(""))
            self.assertFalse(py_utils_string.string_not_blank(" "))
            self.assertTrue(py_utils_string.string_not_blank("s"))
            self.assertTrue(py_utils_string.string_not_blank(" s"))
            self.assertTrue(py_utils_string.string_not_blank("s "))
            self.assertTrue(py_utils_string.string_not_blank(" s "))


if __name__ == "__main__":
    unittest.main(Test)
