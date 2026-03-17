import unittest

import py_utils_json


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_read_json(self):
            json_string = '{"id":"MediaMarco27DataDiscoDVideoAnimeToTransferOnePunchManS1Ita01LUomoPiForteMp401LUomoPiForteMp4284962284","path":"/media/marco27/Data/DiscoD/video/anime/toTransfer/One-Punch Man S1/ita","name":"01 - L’uomo più forte.mp4","namespace":"toTransfer/One-Punch Man S1/ita","mime":"video/mp4","created":"2021-01-03 12:43:35","modified":"2021-01-03 10:47:51","size":284962284}'
            expected = '{"id":"MediaMarco27DataDiscoDVideoAnimeToTransferOnePunchManS1Ita01LUomoPiForteMp401LUomoPiForteMp4284962284","path":"/media/marco27/Data/DiscoD/video/anime/toTransfer/One-Punch Man S1/ita","name":"01 - L’uomo più forte.mp4","namespace":"toTransfer/One-Punch Man S1/ita","mime":"video/mp4","created":"2021-01-03 12:43:35","modified":"2021-01-03 10:47:51","size":284962284}'
            result = py_utils_json.read_json(json_string)
            self.assertEqual(expected, result.__str__())

        def test_write_json_to_file(self):
            json_string = '{"size":284962284}'
            self.assertIsNotNone(self, py_utils_json.write_json_to_file('/Users/marcoguastalli/temp', 'unittest.py.json', json_string))


if __name__ == "__main__":
    unittest.main(Test)
