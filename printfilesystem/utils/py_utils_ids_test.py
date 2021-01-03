import unittest

import py_utils_ids


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_generate_uuid(self):
            self.assertIsNotNone(self, py_utils_ids.generate_uuid())

        def test_generate_name_id(self):
            expected = "MediaMarco27MyBookWd8AnimeAvventuraOnePiece001IniziaLAvventuraMkv123"
            separator = "/"
            path = "/media/marco27/MyBook/wd8/anime/Avventura/One Piece"
            name = "001 - Inizia l\\'avventura.mkv"
            size = 123
            result = py_utils_ids.generate_name_id(separator, path, name, size)
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(Test)
