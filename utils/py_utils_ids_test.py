import unittest

import py_utils_ids


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_generate_uuid(self):
            self.assertIsNotNone(self, py_utils_ids.generate_uuid())

        def test_generate_name_id(self):
            separator = "/"
            path = "/media/marco27/Data/DiscoD/video/anime/One-Punch Man S1/jap"
            file_name = "01 - L’uomo più forte.mp4"
            size = 285299551
            expected = "MediaMarco27DataDiscoDVideoAnimeOnePunchManS1Jap01LUomoPiForteMp4285299551"
            result = py_utils_ids.generate_name_id(separator, path, file_name, size)
            self.assertEqual(expected, result)

        def test_generate_namespace(self):
            path = "/media/marco27/Data/DiscoD/video/anime/One-Punch Man S1/jap"
            file_name = "01 - L’uomo più forte.mp4"
            regexp = "(.*)(anime/)(.*)"
            expected = "One-Punch Man S1/jap"
            result = py_utils_ids.generate_namespace(path, file_name, regexp)
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(Test)
