import unittest

import py_utils


class PyUtilsTest(unittest.TestSuite):
    class GenerateNameIdTests(unittest.TestCase):
        def test_generate_uuid(self):
            self.assertIsNotNone(self, py_utils.generate_uuid())

        def test_generate_name_id(self):
            expected = "MediaMarco27MyBookWd8AnimeAvventuraOnePiece001IniziaLAvventuraMkv123"
            separator = "/"
            path = "/media/marco27/MyBook/wd8/anime/Avventura/One Piece"
            name = "001 - Inizia l\\'avventura.mkv"
            size = 123
            result = py_utils.generate_name_id(separator, path, name, size)
            self.assertEqual(expected, result)

        def test_create_json_array_string_from_string_list(self):
            expected = '["one","two","three"]'
            strings = ["one", "two", "three"]
            result = py_utils.create_json_array_string_from_string_list(strings)
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(PyUtilsTest)
